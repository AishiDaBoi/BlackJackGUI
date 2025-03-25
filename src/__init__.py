from auth.database import get_db_connection

def init_db():
    conn = get_db_connection()
    print("Database initialized successfully!")
    conn.close()

if __name__ == "__main__":
    init_db()