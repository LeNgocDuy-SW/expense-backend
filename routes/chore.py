from fastapi import APIRouter, Depends, HTTPException
from database.database import engine
from auth_helpers import get_current_user 
from model.chore import Chore, ChoreCreate, ChoreRead
from model.user import User
from model.notification import Notification
from sqlmodel import Session, select
import json

router = APIRouter(prefix="/chores", tags=["chore"])

@router.post("", response_model=ChoreRead)
def create_chore(data: ChoreCreate, current_user: User = Depends(get_current_user)):
    if not current_user.room_id or not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Chỉ admin mới được tạo nhiệm vụ")
    
    chore = Chore.model_validate(data, update={"room_id": current_user.room_id})
    
    with Session(engine) as session:
        session.add(chore)
        
        # Notify the assignee
        if chore.assignee_id:
            notif = Notification(
                user_id=chore.assignee_id,
                title="Nhiệm vụ mới",
                message=f"Bạn vừa được giao nhiệm vụ: {chore.name}"
            )
            session.add(notif)
            
        session.commit()
        session.refresh(chore)
        return chore

@router.get("", response_model=list[ChoreRead])
def get_chores(current_user: User = Depends(get_current_user)):
    if not current_user.room_id:
        return []
    with Session(engine) as session:
        return session.exec(select(Chore).where(Chore.room_id == current_user.room_id)).all()

@router.put("/{id}/submit")
def submit_chore(id: int, current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        chore = session.get(Chore, id)
        if not chore or chore.room_id != current_user.room_id:
            raise HTTPException(status_code=404, detail="Không tìm thấy")
        if chore.assignee_id != current_user.id and not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Chỉ người được giao mới được nộp nhiệm vụ")
        
        chore.status = "review"
        session.add(chore)
        
        # Notify admin
        admin = session.exec(select(User).where(User.room_id == current_user.room_id, User.is_admin == True)).first()
        if admin:
            notif = Notification(
                user_id=admin.id,
                title="Nhiệm vụ cần duyệt",
                message=f"{current_user.display_name or current_user.username} đã hoàn thành nhiệm vụ '{chore.name}' và đang chờ bạn duyệt."
            )
            session.add(notif)
            
        session.commit()
        return {"message": "Đã nộp, chờ admin duyệt"}

@router.put("/{id}/approve")
def approve_chore(id: int, current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Chỉ admin mới được duyệt")
    
    with Session(engine) as session:
        chore = session.get(Chore, id)
        if not chore or chore.room_id != current_user.room_id:
            raise HTTPException(status_code=404, detail="Không tìm thấy")
        
        users = session.exec(select(User).where(User.room_id == current_user.room_id)).all()
        if not users:
            raise HTTPException(status_code=400, detail="Không có thành viên nào")
        
        user_list_ids = []
        if chore.user_order:
            try:
                user_list_ids = json.loads(chore.user_order)
            except:
                pass
        
        if not user_list_ids:
            # Fallback to sorted by ID
            user_list_ids = [u.id for u in sorted(users, key=lambda x: x.id)]
        
        # Ensure all IDs actually exist
        valid_ids = [u.id for u in users]
        user_list_ids = [uid for uid in user_list_ids if uid in valid_ids]
        
        # If somehow empty
        if not user_list_ids:
            user_list_ids = valid_ids
        
        current_idx = -1
        try:
            current_idx = user_list_ids.index(chore.assignee_id)
        except ValueError:
            pass
            
        next_user_id = user_list_ids[(current_idx + 1) % len(user_list_ids)]
        
        chore.assignee_id = next_user_id
        chore.status = "pending"
        
        session.add(chore)
        
        # Notify next user
        notif = Notification(
            user_id=next_user_id,
            title="Đến lượt của bạn",
            message=f"Nhiệm vụ '{chore.name}' đã được duyệt. Bây giờ đến lượt bạn thực hiện!"
        )
        session.add(notif)
        
        session.commit()
        session.refresh(chore)
        return chore

@router.delete("/{id}")
def delete_chore(id: int, current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Chỉ admin mới được xóa")
    with Session(engine) as session:
        chore = session.get(Chore, id)
        if not chore or chore.room_id != current_user.room_id:
            raise HTTPException(status_code=404, detail="Không tìm thấy")
        session.delete(chore)
        session.commit()
        return {"message": "Đã xóa"}

from model.chore import ChoreOrderUpdate

@router.put("/{id}/order")
def update_chore_order(id: int, data: ChoreOrderUpdate, current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Chỉ admin mới được đổi thứ tự")
    with Session(engine) as session:
        chore = session.get(Chore, id)
        if not chore or chore.room_id != current_user.room_id:
            raise HTTPException(status_code=404, detail="Không tìm thấy")
        chore.user_order = json.dumps(data.user_order)
        if chore.assignee_id not in data.user_order and len(data.user_order) > 0:
            chore.assignee_id = data.user_order[0]
        session.add(chore)
        session.commit()
        return {"message": "Đã cập nhật thứ tự"}
