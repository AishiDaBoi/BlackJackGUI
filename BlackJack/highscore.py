from db import get_db_connection


def update_highscore(username, rounds_won):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET highscore = GREATEST(highscore, %s) WHERE username = %s", (rounds_won, username))
    conn.commit()

    print("✅ Highscore gespeichert!")
    cursor.close()
    conn.close()

def get_highscore(username):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT highscore FROM users WHERE username = %s", (username,))
    highscore = cursor.fetchone()

    cursor.close()
    conn.close()

    return highscore[0] if highscore and highscore[0] is not None else 0  # Falls None, setze 0 zurück
