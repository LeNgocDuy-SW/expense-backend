from sqlalchemy import create_engine, text

engine = create_engine('postgresql://postgres:duy2005@localhost:5432/expense_app')
with engine.connect() as conn:
    conn.execute(text('ALTER TABLE "user" ADD COLUMN avatar VARCHAR;'))
    conn.commit()
