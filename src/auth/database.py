import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    """Creates and returns a database connection, ensuring tables exist"""
    db_path = os.path.join(os.path.dirname(__file__), '..', 'database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    # Initialize tables if they don't exist
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            credits INTEGER DEFAULT 1000
        )
    """)
    conn.commit()

    return conn