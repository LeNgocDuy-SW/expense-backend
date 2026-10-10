from sqlalchemy import create_engine, text
engine = create_engine('postgresql://postgres:duy2005@localhost:5432/expense_app')
with engine.connect() as conn:
    # 1. Create Room table
    try:
        conn.execute(text('''
            CREATE TABLE IF NOT EXISTS room (
                id SERIAL PRIMARY KEY,
                name VARCHAR NOT NULL,
                invite_code VARCHAR NOT NULL UNIQUE
            );
        '''))
        print("Created room table")
    except Exception as e:
        print("Error creating room:", e)
        
    # 2. Add room_id to user
    try:
        conn.execute(text('ALTER TABLE "user" ADD COLUMN room_id INTEGER REFERENCES room(id)'))
        print("Added room_id to user")
    except Exception as e:
        print("user.room_id may exist:", e)
        
    # 3. Add room_id to purchase
    try:
        conn.execute(text('ALTER TABLE purchase ADD COLUMN room_id INTEGER REFERENCES room(id)'))
        print("Added room_id to purchase")
    except Exception as e:
        print("purchase.room_id may exist:", e)

    # 4. Add room_id to monthlybill
    try:
        conn.execute(text('ALTER TABLE monthlybill ADD COLUMN room_id INTEGER REFERENCES room(id)'))
        print("Added room_id to monthlybill")
    except Exception as e:
        print("monthlybill.room_id may exist:", e)

    conn.commit()
