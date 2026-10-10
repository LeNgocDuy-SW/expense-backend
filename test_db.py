import sys
from sqlmodel import Session, select
from database.database import engine
from model.user import User
try:
    with Session(engine) as session:
        session.exec(select(User)).first()
    print("DB connection successful")
except Exception as e:
    import traceback
    traceback.print_exc()
