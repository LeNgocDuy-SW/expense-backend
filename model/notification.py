from sqlmodel import SQLModel, Field, Session
from database.database import engine
from datetime import datetime, timezone
from typing import Optional

class Notification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    title: str
    message: str
    is_read: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)
    print("Notification table created")
