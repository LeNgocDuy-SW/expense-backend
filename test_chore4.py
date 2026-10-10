from sqlmodel import Session
from database.database import engine
from model.chore import Chore

with Session(engine) as session:
    try:
        chore = Chore(name="Test 2", assignee_id=1, room_id=1)
        session.add(chore)
        session.commit()
        session.refresh(chore)
        print("Chore created:", chore)
    except Exception as e:
        print("Error inserting to DB:", e)
