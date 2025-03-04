import bcrypt
from .database import get_db_connection


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_pw = hash_password(password)

    try:
        cursor.execute("INSERT INTO savefiles (username, password_hash, highscore, credits) VALUES (%s, %s, %s, %s)", (username, hash_password(password), 0, 1000))
        conn.commit()
        return True
    except:
        return False
    finally:
        cursor.close()
        conn.close()

def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM savefiles WHERE username = %s", (username,))
    user = cursor.fetchone()

    cursor.fetchall()
    cursor.close()
    conn.close()

    if user and bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        return True
    return False