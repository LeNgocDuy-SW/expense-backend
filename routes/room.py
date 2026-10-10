from fastapi import APIRouter, Depends, HTTPException
from database.database import engine
from auth_helpers import get_current_user 
from model.room import Room, RoomCreate, RoomRead, RoomJoin
from model.user import User
from sqlmodel import Session, select
import random
import string

router = APIRouter(prefix = "/rooms", tags=["room"])

def generate_invite_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@router.post("", response_model = RoomRead)
def create_room(data: RoomCreate, current_user : User = Depends(get_current_user)):
    if current_user.room_id:
        raise HTTPException(status_code=400, detail="Bạn đã ở trong một phòng rồi")
    with Session(engine) as session:
        room = Room(name=data.name, invite_code=generate_invite_code())
        session.add(room)
        session.commit()
        session.refresh(room)
        
        current_user_db = session.get(User, current_user.id)
        current_user_db.room_id = room.id
        current_user_db.is_admin = True # The creator is admin
        session.add(current_user_db)
        session.commit()
        
        return room

@router.post("/join", response_model = RoomRead)
def join_room(data: RoomJoin, current_user : User = Depends(get_current_user)):
    if current_user.room_id:
        raise HTTPException(status_code=400, detail="Bạn đã ở trong một phòng rồi")
    with Session(engine) as session:
        room = session.exec(select(Room).where(Room.invite_code == data.invite_code)).first()
        if not room:
            raise HTTPException(status_code=404, detail="Không tìm thấy mã phòng này")
        
        current_user_db = session.get(User, current_user.id)
        current_user_db.room_id = room.id
        session.add(current_user_db)
        session.commit()
        
        return room

@router.get("/me", response_model = RoomRead)
def get_my_room(current_user : User = Depends(get_current_user)):
    if not current_user.room_id:
        raise HTTPException(status_code=404, detail="Bạn chưa tham gia phòng nào")
    with Session(engine) as session:
        room = session.get(Room, current_user.room_id)
        return room
