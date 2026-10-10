import sys
from sqlalchemy import text
from database.database import engine

def main():
    try:
        with engine.begin() as conn:
            conn.execute(text('ALTER TABLE "user" ADD COLUMN avatar VARCHAR;'))
        print("Success adding avatar!")
    except Exception as e:
        print(f"Error adding avatar: {e}")

    try:
        with engine.begin() as conn:
            conn.execute(text('ALTER TABLE "user" ADD COLUMN display_name VARCHAR;'))
        print("Success adding display_name!")
    except Exception as e:
        print(f"Error adding display_name: {e}")

if __name__ == "__main__":
    main()
