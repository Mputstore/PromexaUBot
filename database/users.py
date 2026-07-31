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

cursor.execute("""
CREATE TABLE IF NOT EXISTS coin_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    transaction_type TEXT NOT NULL,
    amount INTEGER NOT NULL,
    description TEXT DEFAULT '',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")


def add_column(name, sql):
    cursor.execute("PRAGMA table_info(users)")
    columns = [row[1] for row in cursor.fetchall()]
    if name not in columns:
        cursor.execute(sql)
        print(f"Kolom {name} berhasil dibuat.")


add_column("membership","ALTER TABLE users ADD COLUMN membership TEXT DEFAULT 'Free'")
add_column("coin","ALTER TABLE users ADD COLUMN coin INTEGER DEFAULT 0")
add_column("expired_at","ALTER TABLE users ADD COLUMN expired_at TEXT DEFAULT ''")

conn.commit()
conn.close()


def save_user(user):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE user_id=?", (user.id,))
    if cursor.fetchone():
        conn.close()
        return

    cursor.execute("""
        INSERT INTO users (
            user_id, username, first_name,
            join_date, membership, coin, expired_at
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


def _log_coin(cursor, user_id, tx_type, amount, description=""):
    cursor.execute("""
        INSERT INTO coin_transactions (
            user_id, transaction_type, amount, description
        )
        VALUES (?, ?, ?, ?)
    """, (user_id, tx_type, amount, description))


def add_coin(user_id, amount, tx_type="BONUS", description=""):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET coin = coin + ? WHERE user_id=?",
        (amount, user_id)
    )

    _log_coin(cursor, user_id, tx_type, amount, description)

    conn.commit()
    conn.close()


def spend_coin(user_id, amount, description=""):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT coin FROM users WHERE user_id=?",
        (user_id,)
    )
    row = cursor.fetchone()

    if not row or row[0] < amount:
        conn.close()
        return False

    cursor.execute(
        "UPDATE users SET coin = coin - ? WHERE user_id=?",
        (amount, user_id)
    )

    _log_coin(cursor, user_id, "SPEND", -amount, description)

    conn.commit()
    conn.close()
    return True


def transfer_coin(sender_id, receiver_id, amount):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT coin FROM users WHERE user_id=?", (sender_id,))
    row = cursor.fetchone()

    if not row or row[0] < amount:
        conn.close()
        return False

    cursor.execute(
        "UPDATE users SET coin=coin-? WHERE user_id=?",
        (amount, sender_id)
    )
    cursor.execute(
        "UPDATE users SET coin=coin+? WHERE user_id=?",
        (amount, receiver_id)
    )

    _log_coin(cursor, sender_id, "TRANSFER_OUT", -amount, f"Transfer ke {receiver_id}")
    _log_coin(cursor, receiver_id, "TRANSFER_IN", amount, f"Diterima dari {sender_id}")

    conn.commit()
    conn.close()
    return True


def get_coin_history(user_id, limit=20):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT transaction_type, amount, description, created_at
        FROM coin_transactions
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT ?
    """, (user_id, limit))

    data = cursor.fetchall()
    conn.close()
    return data


def update_membership(user_id, paket):
    paket = paket.lower()

    rewards = {
        "trial": (7, 50),
        "basic": (30, 150),
        "premium": (30, 350)
    }

    hari, bonus = rewards.get(paket, (0, 0))

    expired = (datetime.now() + timedelta(days=hari)).strftime("%d-%m-%Y")

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET membership=?,
            coin=coin+?,
            expired_at=?
        WHERE user_id=?
    """, (paket.title(), bonus, expired, user_id))

    if bonus:
        _log_coin(cursor, user_id, "MEMBERSHIP_BONUS", bonus, f"Bonus paket {paket.title()}")

    conn.commit()
    conn.close()


def get_user(user_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, username, first_name,
               membership, coin, expired_at
        FROM users
        WHERE user_id=?
    """, (user_id,))

    data = cursor.fetchone()
    conn.close()
    return data


def get_total_users():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    total = cursor.fetchone()[0]
    conn.close()
    return total


def get_all_users():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_id, username, first_name
        FROM users
        ORDER BY id ASC
    """)
    data = cursor.fetchall()
    conn.close()
    return data
