import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from database.database import engine
from sqlmodel import Session, text

with Session(engine) as session:
    try:
        session.exec(text("ALTER TABLE chore ADD COLUMN user_order VARCHAR"))
        session.commit()
        print("Column added")
    except Exception as e:
        print("Error:", e)
