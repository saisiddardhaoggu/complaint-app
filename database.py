import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "complaints.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Complaints table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        date TEXT,
        branch TEXT,
        college TEXT,
        description TEXT
    )
    """)

    # Users table (principal login)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT,
        password TEXT
    )
    """)

    # Default principal login create
    cur.execute("SELECT * FROM users")
    if not cur.fetchall():
        cur.execute(
            "INSERT INTO users VALUES (?, ?)",
            ("principal", "admin123")
        )

    conn.commit()
    conn.close()


def insert_complaint(name, phone, date, branch, college, description):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO complaints
    (name, phone, date, branch, college, description)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (name, phone, date, branch, college, description))

    conn.commit()
    conn.close()


def get_complaints():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    SELECT name, branch, college, description, date
    FROM complaints
    ORDER BY id DESC
    """)

    data = cur.fetchall()
    conn.close()
    return data

def update_password(username, new_password):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET password=? WHERE username=?",
        (new_password, username),
    )

    conn.commit()
    conn.close()
