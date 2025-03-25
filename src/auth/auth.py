import bcrypt
from .database import get_db_connection
import sqlite3


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def register_user(username, password):
    try:
        hashed_password = hash_password(password)
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hashed_password)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Username already exists
    finally:
        conn.close()


def login_user(username, password):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT password_hash FROM users WHERE username = ?",
            (username,)
        )
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode(), user['password_hash'].encode()):
            return True
        return False
    finally:
        conn.close()