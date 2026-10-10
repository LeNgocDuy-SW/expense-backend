from sqlmodel import SQLModel
from database.database import engine
# Import tat ca cac models de SQLModel nhan dien
from model.user import User
from model.room import Room
from model.notification import Notification
from model.chore import Chore
from model.monthlybill import MonthlyBill
from model.purchase import Purchase

# Tao tat ca cac bang tren Supabase
SQLModel.metadata.create_all(engine)
print("Tat ca cac bang da duoc tao thanh cong tren Supabase!")
