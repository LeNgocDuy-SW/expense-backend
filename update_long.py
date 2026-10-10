import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from database.database import engine
from sqlmodel import Session
import model.room
import model.user

with Session(engine) as session:
    u = session.get(model.user.User, 3)
    if u:
        u.room_id = 1
        session.add(u)
        session.commit()
        print("Updated Long to room_id 1")
    else:
        print("Long not found")
