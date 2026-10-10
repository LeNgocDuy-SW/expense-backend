from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
import os
import shutil
from database.database import engine
from auth_helpers import get_current_user 

from model.user import User, UserCreate, UserRead, LoginData, ChangePassword, DisplayNameUpdate
from datetime import datetime, timezone
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from pwdlib import PasswordHash
from auth_helpers import password_hash, create_access_token

router = APIRouter(prefix = "", tags =["auth"])

@router.post("/register", response_model = UserRead)
def register(data: UserCreate):
    with Session(engine) as session:
        existing = session.exec(select(User).where(User.username == data.username)).first()
        if existing:
            raise HTTPException(status_code = 400, detail = "Username đã tồn tại")
        clean_username = data.username.strip()
        if " " in clean_username:
            raise HTTPException(status_code = 400, detail = "Username không được chứa từ khóa khoảng trắng")
        if clean_username.lower() == data.password.lower():
            raise HTTPException(status_code = 400, detail = "mật khẩu không được trùng với Username")
        user = User(
            username = clean_username,
            hashed_password = password_hash.hash(data.password)
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

@router.post("/login")
def login(data: LoginData):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == data.username)).first()
        if not user:
            raise HTTPException(status_code=401, detail="Sai username hoặc mật khẩu")
        if not password_hash.verify(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Sai username hoặc mật khẩu")
        token = create_access_token(user.username)
        return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model = UserRead)
def read_me(current_user : User = Depends(get_current_user)):
    return current_user

@router.get("/users", response_model = list[UserRead])
def get_all_users(current_user : User =  Depends(get_current_user)):
    if not current_user.room_id:
        return []
    with Session(engine) as session:
        return session.exec(select(User).where(User.room_id == current_user.room_id)).all()
@router.post("/change-password")
def change_password(data: ChangePassword, current_user : User = Depends(get_current_user)):
    if not password_hash.verify(data.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Mật khẩu cũ không chính xác")
    if data.old_password == data.new_password:
        raise HTTPException(status_code=400, detail="Mật khẩu mới không được trùng với mật khẩu cũ")
    with Session(engine) as session:
        db_user = session.get(User, current_user.id)
        db_user.hashed_password = password_hash.hash(data.new_password)
        session.add(db_user)
        session.commit()
    return {"message": "Đổi mk thành công"}

@router.put("/users/me", response_model=UserRead)
def update_display_name(data: DisplayNameUpdate, current_user: User = Depends(get_current_user)):
    clean_name = data.display_name.strip()
    with Session(engine) as session:
        db_user = session.get(User, current_user.id)
        db_user.display_name = clean_name
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

@router.delete("/users/{id}")
def delete_user(id: int, current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Chỉ admin mới có quyền xóa thành viên")
    if current_user.id == id:
        raise HTTPException(status_code=400, detail="Không thể tự xóa chính mình")
    
    with Session(engine) as session:
        user_to_delete = session.get(User, id)
        if not user_to_delete:
            raise HTTPException(status_code=404, detail="Không tìm thấy thành viên")
        
        # We might need to delete related data or set them to null. 
        # But for now, we just delete the user.
        try:
            session.delete(user_to_delete)
            session.commit()
            return {"message": "Đã xóa thành viên"}
        except IntegrityError:
            session.rollback()
            raise HTTPException(status_code=400, detail="Không thể xóa thành viên vì họ đang có dữ liệu liên quan (khoản chi tiêu, ghi chú, v.v...)")

@router.post("/users/me/avatar", response_model=UserRead)
def upload_avatar(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ file hình ảnh")
    
    file_extension = file.filename.split(".")[-1]
    avatar_filename = f"avatar_{current_user.id}.{file_extension}"
    file_location = f"avatars/{avatar_filename}"
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    with Session(engine) as session:
        db_user = session.get(User, current_user.id)
        db_user.avatar = f"/avatars/{avatar_filename}"
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
