from db import get_db_connection

def update_highscore(username, rounds_won):
    """
    Updates the user's high score in the database.
    If the new score is higher than the existing one, it gets updated.

    Args:
        username (str): The username of the player.
        rounds_won (int): The number of rounds won to be considered for the high score.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET highscore = GREATEST(highscore, %s) WHERE username = %s",
        (rounds_won, username)
    )
    conn.commit()

    print("High score saved.")
    cursor.close()
    conn.close()

def get_highscore(username):
    """
    Retrieves the user's high score from the database.

    Args:
        username (str): The username of the player.

    Returns:
        int: The user's high score, or 0 if no score is found.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT highscore FROM users WHERE username = %s", (username,))
    highscore = cursor.fetchone()

    cursor.close()
    conn.close()

    return highscore[0] if highscore and highscore[0] is not None else 0  # Return 0 if no score is found
