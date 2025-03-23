import sqlite3
from config import DATABASE_PATH

def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    return conn

def get_user_by_telegram_id(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def register_user(telegram_id, username, first_name, avatar_url):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (telegram_id, username, first_name, avatar_url, registered_at) VALUES (?, ?, ?, ?, datetime('now'))",
        (telegram_id, username, first_name, avatar_url)
    )
    conn.commit()
    conn.close()
