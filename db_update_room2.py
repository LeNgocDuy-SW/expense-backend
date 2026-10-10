from sqlalchemy import create_engine, text
engine = create_engine('postgresql://postgres:duy2005@localhost:5432/expense_app')
with engine.connect() as conn:
    # Check if a room exists
    res = conn.execute(text('SELECT id FROM room LIMIT 1')).fetchone()
    if not res:
        conn.execute(text("INSERT INTO room (name, invite_code) VALUES ('Phòng Mặc Định', 'ROOM123')"))
        res = conn.execute(text('SELECT id FROM room LIMIT 1')).fetchone()
        
    default_room_id = res[0]
    
    # Update existing records
    conn.execute(text(f'UPDATE "user" SET room_id = {default_room_id} WHERE room_id IS NULL'))
    conn.execute(text(f'UPDATE purchase SET room_id = {default_room_id} WHERE room_id IS NULL'))
    conn.execute(text(f'UPDATE monthlybill SET room_id = {default_room_id} WHERE room_id IS NULL'))
    conn.commit()
    print("Migrated existing data to default room")
