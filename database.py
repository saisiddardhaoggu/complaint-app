import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")


def get_conn():
    return psycopg2.connect(DATABASE_URL)


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS complaints (
        name TEXT,
        phone TEXT,
        branch TEXT,
        college TEXT,
        description TEXT,
        date TEXT
    )
    """)

    cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
""")


    cur.execute("SELECT * FROM users WHERE username=%s", ("principal",))
    if not cur.fetchone():
     cur.execute(
        "INSERT INTO users VALUES (%s,%s)",
        ("principal", "admin123"),
    )


def insert_complaint(name, phone, branch, college, description, date):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO complaints VALUES (%s,%s,%s,%s,%s,%s)",
        (name, phone, branch, college, description, date),
    )

    conn.commit()
    conn.close()


def get_complaints():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM complaints")
    data = cur.fetchall()

    conn.close()
    return data

def update_password(new_password):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET password=%s WHERE username=%s",
        (new_password, "principal"),
    )

    conn.commit()
    conn.close()
