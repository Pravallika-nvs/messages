import sqlite3

conn = sqlite3.connect("messages.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT NOT NULL,
    created_at TEXT NOT NULL
)
""")

conn.commit()
conn.close()