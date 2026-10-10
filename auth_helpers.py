from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Depends
from sqlmodel import Session, select
import jwt
import os
from pwdlib import PasswordHash
from dotenv import load_dotenv
from model.user import User
from datetime import datetime, timedelta, timezone
from database.database import engine

load_dotenv()  # đọc file .env, nạp vào os.environ
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256") # "HS256" là giá trị mặc định nếu không tìm thấy trong .env

password_hash = PasswordHash.recommended()

def create_access_token(username : str) -> str:
    payload = {
        "sub": username,
        "exp": datetime.now(timezone.utc) + timedelta(days = 15)
    }   
    return jwt.encode(payload, SECRET_KEY, algorithm = ALGORITHM)
security = HTTPBearer()
def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        username = payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code = 401, detail = "Token đã hết hạn")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code = 401, detail = "Token không hợp lệ")
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == username)).first()
        if not user : 
            raise HTTPException(status_code = 401, detail = "Không tìm thấy User")
        return user