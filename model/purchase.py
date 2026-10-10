from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional
from datetime import datetime, timedelta, timezone



class PurchaseCreate(SQLModel):
    description: str 
    amount: float = Field(gt = 0)
    shared_with: Optional[str] = Field(default=None)

class Purchase(PurchaseCreate,  table = True):
    id: Optional[int] = Field(default = None, primary_key = True)
    created_at: Optional[datetime] = Field(default_factory = lambda: datetime.now(timezone.utc))
    buyer_id: Optional[int] = Field(default = None, foreign_key = "user.id")
    room_id: Optional[int] = Field(default=None, foreign_key="room.id")

class PurchaseRead(SQLModel):
    id : int
    description: str 
    amount: float
    created_at: datetime
    buyer_id: int
    room_id: Optional[int] = None
    shared_with: Optional[str] = None

