from sqlmodel import SQLModel, Field
from typing import Optional
class UserCreate(SQLModel):
    username: str = Field(min_length= 3)
    password: str = Field(min_length = 6)

class User(SQLModel, table = True):
    id : Optional[int] = Field(default = None, primary_key = True)
    username : str = Field(unique = True, index = True)
    hashed_password : str
    display_name : Optional[str] = Field(default=None)
    is_admin: bool = Field(default=False)
    room_id: Optional[int] = Field(default=None, foreign_key="room.id")
    avatar: Optional[str] = Field(default=None)

class UserRead(SQLModel):
    id : int
    username: str
    display_name: Optional[str] = None
    is_admin: bool = False
    room_id: Optional[int] = None
    avatar: Optional[str] = None

class LoginData(SQLModel):
     username : str
     password: str

class ChangePassword(SQLModel):
    old_password: str
    new_password: str = Field(min_length = 6)

class DisplayNameUpdate(SQLModel):
    display_name: str = Field(min_length = 1)