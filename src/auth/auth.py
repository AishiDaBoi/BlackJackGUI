import bcrypt
import sqlite3  # Assuming you're using SQLite for storing user data

# Utility function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('your_database.db')  # Replace with your actual database path
    return conn

# Function to hash a password
def hash_password(password):
    # bcrypt.gensalt() generates a new salt, and hashpw() hashes the password with that salt
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Function to register a user
def register_user(username, password):
    hashed_password = hash_password(password)  # Hash the password before storing it
    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert the username and hashed password into the database
    cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    cursor.close()
    conn.close()

# Function to login a user
def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Assuming SQLite (use a dictionary-based cursor)

    # Select user by username
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        stored_hash = user['password_hash']
        try:
            # Check if the provided password matches the stored hash
            if bcrypt.checkpw(password.encode(), stored_hash.encode()):
                return True  # Successful login
            else:
                print("Incorrect password.")
                return False  # Incorrect password
        except ValueError as e:
            print(f"Error checking password: {e}")
            return False  # Error with password hash comparison

    else:
        print("User not found.")
        return False  # User not found in database
