from typing import Optional
from sqlmodel import SQLModel, Field

class Room(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    invite_code: str = Field(unique=True, index=True)

class RoomCreate(SQLModel):
    name: str

class RoomRead(SQLModel):
    id: int
    name: str
    invite_code: str

class RoomJoin(SQLModel):
    invite_code: str
