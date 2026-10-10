import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from database.database import engine
from sqlmodel import Session, select
import model.room
import model.user
import model.chore

with Session(engine) as session:
    chore = session.get(model.chore.Chore, 1) # Assuming chore 1 exists
    if chore:
        users = session.exec(select(model.user.User).where(model.user.User.room_id == chore.room_id).order_by(model.user.User.id)).all()
        current_idx = next((i for i, u in enumerate(users) if u.id == chore.assignee_id), -1)
        next_user = users[(current_idx + 1) % len(users)]
        print(f"Current assignee: {chore.assignee_id}, Next assignee: {next_user.id}")
        chore.assignee_id = next_user.id
        session.add(chore)
        session.commit()
    else:
        print("Chore 1 not found")
