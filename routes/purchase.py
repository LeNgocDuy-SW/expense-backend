from fastapi import APIRouter, Depends, HTTPException
from database.database import engine
from auth_helpers import get_current_user 
from model.purchase import PurchaseCreate, Purchase, PurchaseRead
from model.user import User
from sqlmodel import Session, select

router = APIRouter(prefix = "/purchases", tags=["purchase"])

@router.post("", response_model = PurchaseRead)
def create_purchase(data: PurchaseCreate, current_user : User = Depends(get_current_user)):
    if not current_user.room_id:
        raise HTTPException(status_code=400, detail="Bạn chưa tham gia phòng nào")
    purchase = Purchase.model_validate(data)
    purchase.buyer_id = current_user.id
    purchase.room_id = current_user.room_id
    with Session(engine) as session:
        session.add(purchase)
        session.commit()
        session.refresh(purchase)
        return purchase

@router.get("", response_model = list[PurchaseRead])
def get_purchases( current_user: User = Depends(get_current_user)):
    if not current_user.room_id:
        return []
    with Session(engine) as session:
        return session.exec(select(Purchase).where(Purchase.room_id == current_user.room_id)).all()

@router.get("/{id}", response_model = PurchaseRead)
def get_purchase(id: int,  current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        pur = session.get(Purchase, id)
        if not pur or pur.room_id != current_user.room_id:
            raise HTTPException(status_code=404, detail="Không tìm thấy")
        return pur

@router.put("/{id}", response_model = PurchaseRead)
def update_purchase(id : int, data: PurchaseCreate, current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        pur = session.get(Purchase, id)
        if not pur or pur.room_id != current_user.room_id: 
            raise HTTPException(status_code=404, detail="Không tìm thấy")
        if pur.buyer_id != current_user.id and not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Không có quyền")
        pur.description = data.description
        pur.amount = data.amount
        pur.shared_with = data.shared_with
        session.add(pur)
        session.commit()
        session.refresh(pur)
        return pur

@router.delete("/{id}")
def delete_purchase(id: int, current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        pur = session.get(Purchase, id)
        if not pur or pur.room_id != current_user.room_id:
            raise HTTPException(status_code=404, detail="Không tìm thấy")
        if pur.buyer_id != current_user.id and not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Không có quyền")
        session.delete(pur)
        session.commit()
        return {"message": "Đã xóa"}