import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Erstellt eine Verbindung zur MySQL-Datenbank."""
    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT")))
    except mysql.connector.Error as err:
        print(f"Fehler bei der Verbindung zur Datenbank: {err}")
        return None