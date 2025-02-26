import bcrypt
import mysql.connector

from .database import get_db_connection


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_pw = hash_password(password)

    try:
        cursor.execute(
            "INSERT INTO savefiles (username, password_hash, highscore, credits) VALUES (%s, %s, %s, %s)",
            (username, hashed_pw, 0, 1000)  # Standardwerte: highscore = 0, credits = 1000
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:  # Spezifische Fehlerbehandlung
        print(f"Fehler bei der Registrierung: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM savefiles WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
            return True
        return False
    except mysql.connector.Error as err:
        print(f"Fehler beim Login: {err}")
        return False
    finally:
        cursor.close()
        conn.close()