# loginViaJson.py:
# This file is used to login to the game using a json file.
# The json file contains the username, password and highscore (max. rounds won) of the user.
# The user can login using the username and password from the json file.
#

import json
import bcrypt
import os
from auth import hash_password, login_user, register_user

JSON_FILE = "users.json"


def load_users():
    """Lädt die Benutzer aus der JSON-Datei und behandelt leere Dateien."""
    if not os.path.exists(JSON_FILE):
        return {}  # Falls Datei nicht existiert, leeres Dict zurückgeben

    try:
        with open(JSON_FILE, "r") as file:
            data = file.read().strip()  # Leere Zeichen entfernen
            if not data:  # Falls die Datei leer ist
                print("Keine Login-Information in der JSON-Datei gefunden.")
                return {}
            return json.loads(data)  # JSON-Daten laden
    except json.JSONDecodeError:
        print("Fehler: Ungültige JSON-Datei. Setze Datei zurück.")
        save_users({})  # Setze Datei zurück auf ein leeres JSON-Objekt
        return {}



def save_users(users):
    """Speichert die Benutzer in der JSON-Datei."""
    with open(JSON_FILE, "w") as file:
        json.dump(users, file, indent=4)


def json_register(username, password):
    """Registriert einen Benutzer in der JSON-Datei."""
    users = load_users()

    if username in users:
        print("Benutzer existiert bereits in der JSON-Datei!")
        return False

    users[username] = {
        "password": hash_password(password),
        "highscore": 0
    }
    save_users(users)
    print("Benutzer erfolgreich in JSON registriert!")
    return True


def json_login(username, password):
    """Überprüft die Anmeldedaten in der JSON-Datei."""
    users = load_users()

    if username in users and bcrypt.checkpw(password.encode(), users[username]["password"].encode()):
        print("Login über JSON erfolgreich!")
        return True
    print("Falsche Anmeldeinformationen für JSON-Login.")
    return False


def register(username, password, use_json=False):
    """Registriert einen Benutzer entweder in der JSON-Datei oder der MySQL-Datenbank."""
    if use_json:
        return json_register(username, password)
    else:
        return register_user(username, password)


def login(username, password, use_json=False):
    """Meldet einen Benutzer entweder über JSON oder die MySQL-Datenbank an."""
    if use_json:
        return json_login(username, password)
    else:
        return login_user(username, password)
