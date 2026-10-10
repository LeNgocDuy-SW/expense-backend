from sqlmodel import SQLModel
from database.database import engine
import model.user
import model.purchase
import model.monthlybill
import model.room
import model.chore

SQLModel.metadata.create_all(engine)
print("Created missing tables")
