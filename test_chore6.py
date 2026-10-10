import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from sqlmodel import Session, select
from database.database import engine
from model.user import User
from auth_helpers import create_access_token
import requests

with Session(engine) as session:
    user = session.exec(select(User).where(User.username == "duyle")).first()
    if user:
        token = create_access_token({"sub": user.username})
        headers = {"Authorization": f"Bearer {token}"}
        res2 = requests.post("http://localhost:8000/chores", json={"name": "Test chore", "assignee_id": user.id}, headers=headers)
        print("Chores API status:", res2.status_code)
        print("Chores API response:", res2.text)
    else:
        print("User not found")
