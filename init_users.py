import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# 🚨 Drop the old table if it exists
cursor.execute('DROP TABLE IF EXISTS users')

# ✅ Create the correct table
cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

conn.commit()
conn.close()

