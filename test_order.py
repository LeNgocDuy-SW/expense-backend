import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from database.database import engine
from sqlmodel import Session, select
import model.room
import model.user
import model.chore

with Session(engine) as session:
    chore = session.exec(select(model.chore.Chore)).first()
    if chore:
        print("Chore ID:", chore.id)
        print("Old user_order:", chore.user_order)
        # Update manually
        chore.user_order = "[2, 1, 3]"
        session.add(chore)
        session.commit()
        session.refresh(chore)
        print("New user_order:", chore.user_order)
    else:
        print("No chores found")
