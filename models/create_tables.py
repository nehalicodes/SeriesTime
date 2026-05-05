import sqlite3

conn = sqlite3.connect("series.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
);
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS watchlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    show_id INTEGER,
    show_name TEXT,
    poster_path TEXT
);
""")

conn.commit()
conn.close()

print("Tables created successfully!")