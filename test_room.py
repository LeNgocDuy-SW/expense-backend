import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from sqlmodel import Session, select
from database.database import engine
from model.room import Room
from model.user import User

with Session(engine) as session:
    try:
        room = Room(name="Test 3", invite_code="CODE1234")
        session.add(room)
        session.commit()
        session.refresh(room)
        
        u = session.exec(select(User)).first()
        u.room_id = room.id
        session.add(u)
        session.commit()
        print("Success")
    except Exception as e:
        print("Error:", e)
