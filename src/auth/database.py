import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Erstellt eine Verbindung zur SQLite-Datenbank."""
    db_path = os.getenv("DB_PATH", "database.db")  # Standard ist 'database.db'
    return sqlite3.connect(db_path)
