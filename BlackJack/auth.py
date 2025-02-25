# auth.py

import bcrypt
from db import get_db_connection

# 🔑 Passwort hashen
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# ✅ Benutzer registrieren
def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_pw = hash_password(password)

    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed_pw))
        conn.commit()
        print("✅ Benutzer erfolgreich registriert!")
    except Exception as e:
        print(f"❌ Fehler: {e}")
    finally:
        cursor.close()
        conn.close()

# 🔑 Login-Funktion
def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user and bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        print("✅ Login erfolgreich!")
        return True
    else:
        print("❌ Falsche Anmeldedaten!")
        return False
