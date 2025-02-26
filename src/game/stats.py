from ..auth.database import get_db_connection

def get_balance(username):
    """Holt das aktuelle Guthaben eines Spielers aus der Datenbank."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT credits FROM savefiles WHERE username = %s", (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

def update_balance(username, amount):
    """Aktualisiert das Guthaben eines Spielers."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE savefiles SET credits = %s WHERE username = %s", (amount, username))
    conn.commit()
    conn.close()

def get_highscore(username):
    """Holt den Highscore (maximale gewonnene Runden) aus der Datenbank."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT highscore FROM savefiles WHERE username = %s", (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

def update_highscore(username, rounds_won):
    """Aktualisiert den Highscore, falls die aktuelle Rundenzahl höher ist."""
    current_highscore = get_highscore(username)
    if rounds_won > current_highscore:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE savefiles SET highscore = %s WHERE username = %s", (rounds_won, username))
        conn.commit()
        conn.close()
