from database.database import engine
from sqlmodel import Session
from sqlalchemy import text

with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE purchase ADD COLUMN shared_with VARCHAR"))
        conn.commit()
        print("Added shared_with to postgres successfully")
    except Exception as e:
        print("Error:", e)
