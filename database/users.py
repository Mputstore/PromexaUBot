import sqlite3
from datetime import datetime, timedelta

DB_NAME = "users.db"


def connect():
    return sqlite3.connect(DB_NAME)


# ==========================
# MEMBUAT / UPDATE DATABASE
# ==========================

conn = connect()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    username TEXT,
    first_name TEXT,
    join_date TEXT,
    membership TEXT DEFAULT 'Free',
    coin INTEGER DEFAULT 0,
    expired_at TEXT DEFAULT ''
)
""")


def add_column(name, sql):
    cursor.execute("PRAGMA table_info(users)")
    columns = [row[1] for row in cursor.fetchall()]

    if name not in columns:
        cursor.execute(sql)
        print(f"✅ Kolom {name} berhasil dibuat.")


add_column(
    "membership",
    "ALTER TABLE users ADD COLUMN membership TEXT DEFAULT 'Free'"
)

add_column(
    "coin",
    "ALTER TABLE users ADD COLUMN coin INTEGER DEFAULT 0"
)

add_column(
    "expired_at",
    "ALTER TABLE users ADD COLUMN expired_at TEXT DEFAULT ''"
)

conn.commit()
conn.close()


# ==========================
# SIMPAN USER
# ==========================

def save_user(user):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE user_id=?",
        (user.id,)
    )

    if cursor.fetchone():
        conn.close()
        return

    cursor.execute("""
        INSERT INTO users (
            user_id,
            username,
            first_name,
            join_date,
            membership,
            coin,
            expired_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user.id,
        user.username or "",
        user.first_name or "",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Free",
        0,
        ""
    ))

    conn.commit()
    conn.close()


# ==========================
# UPDATE MEMBERSHIP
# ==========================

def update_membership(user_id, paket):

    paket = paket.lower()

    if paket == "trial":
        hari = 7
        coin = 50

    elif paket == "basic":
        hari = 30
        coin = 150

    elif paket == "premium":
        hari = 30
        coin = 350

    else:
        hari = 0
        coin = 0

    expired = (
        datetime.now() +
        timedelta(days=hari)
    ).strftime("%d-%m-%Y")

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET
            membership=?,
            coin=coin+?,
            expired_at=?
        WHERE user_id=?
    """, (
        paket.title(),
        coin,
        expired,
        user_id
    ))

    conn.commit()
    conn.close()


# ==========================
# AMBIL USER
# ==========================

def get_user(user_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            user_id,
            username,
            first_name,
            membership,
            coin,
            expired_at
        FROM users
        WHERE user_id=?
    """, (user_id,))

    data = cursor.fetchone()

    conn.close()

    return data


# ==========================
# TOTAL USER
# ==========================

def get_total_users():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM users"
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total


# ==========================
# SEMUA USER
# ==========================

def get_all_users():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            user_id,
            username,
            first_name
        FROM users
        ORDER BY id ASC
    """)

    data = cursor.fetchall()

    conn.close()

    return data