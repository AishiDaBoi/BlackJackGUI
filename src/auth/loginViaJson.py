import logging
import os
import json

JSON_FILE = "users.json"


logging.basicConfig(level=logging.INFO)

def load_users():
    """Lädt Benutzer aus JSON-Datei."""
    if not os.path.exists(JSON_FILE):
        return {}
    try:
        with open(JSON_FILE, "r") as file:
            data = json.load(file)
            return data
    except json.JSONDecodeError as err:
        logging.error(f"Fehler beim Laden der JSON-Datei: {err}")
        return {}
    except Exception as err:
        logging.error(f"Unerwarteter Fehler: {err}")
        return {}

def save_users(users):
    """Speichert Benutzer in JSON-Datei."""
    try:
        with open(JSON_FILE, "w") as file:
            json.dump(users, file, indent=4)
    except Exception as err:
        logging.error(f"Fehler beim Speichern der JSON-Datei: {err}")

def register_user_json(username, password):
    """Registriert Benutzer in JSON."""
    users = load_users()
    if username in users:
        return False

    users[username] = {"password": bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(), "highscore": 0, credits(): "1000"}
    save_users(users)
    return True

def login_user_json(username, password):
    """Loggt Benutzer über JSON ein."""
    users = load_users()
    if username in users and bcrypt.checkpw(password.encode(), users[username]["password"].encode()):
        return True
    return False
