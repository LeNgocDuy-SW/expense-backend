from sqlmodel import SQLModel
from database.database import engine
from model.user import User
from model.room import Room
from model.notification import Notification

SQLModel.metadata.create_all(engine)
print("Notification table created")
