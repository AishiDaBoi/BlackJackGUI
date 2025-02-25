import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

def get_db_connection():
    """
    Establishes a connection to the MySQL database using credentials
    stored in environment variables.

    Returns:
        mysql.connector.connection.MySQLConnection: A connection object to interact with the database.
    """
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),       # Database host (e.g., localhost or remote server)
        user=os.getenv("DB_USER"),       # Database username
        password=os.getenv("DB_PASSWORD"), # Database password
        database=os.getenv("DB_NAME"),   # Database name
        port=int(os.getenv("DB_PORT"))   # Database port (converted to an integer)
    )
