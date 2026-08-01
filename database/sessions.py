import sqlite3
from datetime import datetime

DB_NAME = "users.db"


def connect():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# ==========================
# CREATE TABLE
# ==========================

conn = connect()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS telegram_sessions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    api_id TEXT NOT NULL,
    api_hash TEXT NOT NULL,
    phone_number TEXT,
    session_name TEXT NOT NULL,
    first_name TEXT,
    last_name TEXT,
    username TEXT,
    is_connected INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()


# ==========================
# SAVE SESSION
# ==========================

def save_session(
    user_id,
    api_id,
    api_hash,
    phone_number,
    session_name,
    first_name="",
    last_name="",
    username=""
):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO telegram_sessions(
            user_id,
            api_id,
            api_hash,
            phone_number,
            session_name,
            first_name,
            last_name,
            username,
            is_connected,
            updated_at
        )
        VALUES(
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
    """, (
        user_id,
        api_id,
        api_hash,
        phone_number,
        session_name,
        first_name,
        last_name,
        username,
        1,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


# ==========================
# GET SESSION
# ==========================

def get_session(user_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM telegram_sessions
        WHERE user_id=?
    """, (user_id,))

    data = cursor.fetchone()

    conn.close()

    return data


# ==========================
# CHECK SESSION
# ==========================

def session_exists(user_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM telegram_sessions
        WHERE user_id=?
    """, (user_id,))

    result = cursor.fetchone()

    conn.close()

    return result is not None


# ==========================
# CONNECTION STATUS
# ==========================

def is_connected(user_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT is_connected
        FROM telegram_sessions
        WHERE user_id=?
    """, (user_id,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return bool(row["is_connected"])

    return False
# ==========================
# UPDATE SESSION
# ==========================

def update_session(
    user_id,
    phone_number=None,
    first_name=None,
    last_name=None,
    username=None,
    session_name=None
):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE telegram_sessions
        SET
            phone_number = COALESCE(?, phone_number),
            first_name = COALESCE(?, first_name),
            last_name = COALESCE(?, last_name),
            username = COALESCE(?, username),
            session_name = COALESCE(?, session_name),
            updated_at = ?
        WHERE user_id = ?
    """, (
        phone_number,
        first_name,
        last_name,
        username,
        session_name,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        user_id
    ))

    conn.commit()
    conn.close()


# ==========================
# UPDATE STATUS
# ==========================

def update_status(user_id, status):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE telegram_sessions
        SET
            is_connected = ?,
            updated_at = ?
        WHERE user_id = ?
    """, (
        1 if status else 0,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        user_id
    ))

    conn.commit()
    conn.close()


# ==========================
# DELETE SESSION
# ==========================

def delete_session(user_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM telegram_sessions
        WHERE user_id = ?
    """, (user_id,))

    conn.commit()
    conn.close()


# ==========================
# GET ALL SESSIONS
# ==========================

def get_all_sessions():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM telegram_sessions
        ORDER BY id ASC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


# ==========================
# GET SESSION NAME
# ==========================

def get_session_name(user_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT session_name
        FROM telegram_sessions
        WHERE user_id = ?
    """, (user_id,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return row["session_name"]

    return None


# ==========================
# GET PHONE NUMBER
# ==========================

def get_phone_number(user_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT phone_number
        FROM telegram_sessions
        WHERE user_id = ?
    """, (user_id,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return row["phone_number"]

    return None


# ==========================
# CONNECT SESSION
# ==========================

def connect_session(user_id):

    update_status(user_id, True)


# ==========================
# DISCONNECT SESSION
# ==========================

def disconnect_session(user_id):

    update_status(user_id, False)


# ==========================
# COUNT CONNECTED SESSION
# ==========================

def count_connected_sessions():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM telegram_sessions
        WHERE is_connected = 1
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total  