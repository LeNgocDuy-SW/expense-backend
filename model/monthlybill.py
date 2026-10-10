from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

class MonthlyBillCreate(SQLModel):
    electricity_quantity: int = Field(gt = 0)
    water_quantity : int
    rent_amount: int = 3500000
    other_amount: int = 200000
    wifi_amount: int = 100000
    parking_amount: int = 400000
    electricity_price: int = 4000
    water_price: int = 35000

class MonthlyBill(MonthlyBillCreate, table = True):
    id: Optional[int] = Field(default = None, primary_key = True)
    month: Optional[int] = Field(default = None, ge = 1, le = 12)
    year: Optional[int] = Field(default = None, ge = 2025, le = 2030)
    created_at : Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    room_id: Optional[int] = Field(default=None, foreign_key="room.id")
class MonthlyBillRead(SQLModel):
    id : int
    electricity_quantity: int 
    water_quantity : int
    rent_amount: int 
    other_amount: int 
    wifi_amount: int 
    parking_amount: int 
    month: int
    year: int
    water_price: int 
    created_at: datetime
    electricity_price: int 
    room_id: Optional[int] = None


