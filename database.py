import sqlite3

DB_NAME = "complaints.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    # Admin table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)

    # Default admin
    user = conn.execute("SELECT * FROM admin WHERE username='principal'").fetchone()
    if not user:
        conn.execute(
            "INSERT INTO admin (username, password) VALUES (?, ?)",
            ("principal", "admin123")
        )

    # Complaints table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            branch TEXT,
            college TEXT,
            description TEXT,
            date TEXT
        )
    """)

    conn.commit()
    conn.close()