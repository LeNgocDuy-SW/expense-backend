from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
import model.room

class ChoreCreate(SQLModel):
    name: str
    assignee_id: int

class Chore(ChoreCreate, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    room_id: int = Field(foreign_key="room.id")
    status: str = Field(default="pending") # "pending", "review"
    user_order: Optional[str] = Field(default=None) # JSON list of user IDs
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ChoreRead(SQLModel):
    id: int
    name: str
    assignee_id: int
    room_id: int
    status: str
    user_order: Optional[str] = None
    created_at: datetime

class ChoreOrderUpdate(SQLModel):
    user_order: list[int]
