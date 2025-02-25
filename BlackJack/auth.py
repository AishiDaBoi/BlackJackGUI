import bcrypt
from db import get_db_connection

# Hash a password
def hash_password(password):
    """
    Hashes a password using bcrypt.

    Args:
        password (str): The plaintext password.

    Returns:
        str: The hashed password.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Register a new user
def register_user(username, password):
    """
    Registers a new user by storing their username and hashed password in the database.

    Args:
        username (str): The username of the new user.
        password (str): The plaintext password to be hashed and stored.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_pw = hash_password(password)

    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed_pw))
        conn.commit()
        print("User registered successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Login function
def login_user(username, password):
    """
    Authenticates a user by checking the provided password against the stored hash.

    Args:
        username (str): The username of the user.
        password (str): The plaintext password to be verified.

    Returns:
        bool: True if authentication is successful, False otherwise.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user and bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        print("Login successful.")
        return True
    else:
        print("Incorrect login credentials.")
        return False
