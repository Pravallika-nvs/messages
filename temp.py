import sqlite3

conn = sqlite3.connect("messages.db")

cursor = conn.cursor()

cursor.execute("SELECT * FROM messages")

print(cursor.fetchall())

conn.close()