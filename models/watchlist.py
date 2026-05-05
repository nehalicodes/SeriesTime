from models.database import get_db

def add_to_watchlist(user_id, show_id, show_name, poster):
    conn = get_db()
    conn.execute(
        "INSERT INTO watchlist (user_id, show_id, show_name, poster_path) VALUES (?, ?, ?, ?)",
        (user_id, show_id, show_name, poster)
    )
    conn.commit()
    conn.close()

def get_watchlist(user_id):
    conn = get_db()
    items = conn.execute(
        "SELECT * FROM watchlist WHERE user_id = ?",
        (user_id,)
    ).fetchall()
    conn.close()
    return items