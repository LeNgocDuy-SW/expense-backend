import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from sqlalchemy import create_engine, text
engine = create_engine('postgresql://postgres:duy2005@localhost:5432/expense_app')
with engine.connect() as conn:
    # Add is_admin column if it doesn't exist
    try:
        conn.execute(text('ALTER TABLE "user" ADD COLUMN is_admin BOOLEAN DEFAULT FALSE'))
        print("Added is_admin column")
    except Exception as e:
        print("is_admin probably exists", e)
    
    # Update user 'Duy' or similar to 'duyle' and make admin
    conn.execute(text('UPDATE "user" SET username = \'duyle\', is_admin = TRUE WHERE username = \'Duy\' OR username = \'duyle\''))
    conn.commit()
    
    res = conn.execute(text('SELECT id, username, display_name, is_admin FROM "user"'))
    print("Users after:")
    for r in res:
        print(r)
