import sqlite3
conn = sqlite3.connect('app_expense.db')
c = conn.cursor()
try:
    c.execute("ALTER TABLE purchase ADD COLUMN shared_with VARCHAR")
    print("Added shared_with column successfully")
except Exception as e:
    print(e)
conn.commit()
conn.close()
