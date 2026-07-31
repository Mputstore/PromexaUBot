import sqlite3
import uuid
from datetime import datetime


DB_NAME = "users.db"


def connect():
    return sqlite3.connect(DB_NAME)


# ==========================
# MEMBUAT TABEL
# ==========================

conn = connect()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice TEXT,
    user_id INTEGER,
    username TEXT,
    layanan TEXT,
    lpm INTEGER,
    durasi TEXT,
    harga INTEGER,
    promosi TEXT,
    status TEXT,
    created_at TEXT
)
""")

conn.commit()
conn.close()


# ==========================
# SIMPAN ORDER
# ==========================

def save_order(user_id, username, layanan, lpm, durasi, harga, promosi):

    conn = connect()
    cursor = conn.cursor()

    invoice = "INV-" + uuid.uuid4().hex[:8].upper()

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO orders (
            invoice,
            user_id,
            username,
            layanan,
            lpm,
            durasi,
            harga,
            promosi,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        invoice,
        user_id,
        username,
        layanan,
        lpm,
        durasi,
        harga,
        promosi,
        "Menunggu Pembayaran",
        created_at
    ))

    conn.commit()
    conn.close()

    return invoice


# ==========================
# DASHBOARD
# ==========================

def get_pending_orders():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM orders WHERE status=?",
        ("Menunggu Pembayaran",)
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_total_income():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COALESCE(SUM(harga),0) FROM orders WHERE status=?",
        ("Lunas",)
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_total_users():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(DISTINCT user_id) FROM orders"
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total


# ==========================
# LIST ORDER
# ==========================

def get_all_orders():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            invoice,
            username,
            layanan,
            harga,
            status
        FROM orders
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


def get_pending_orders_list():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            invoice,
            username,
            layanan,
            harga,
            status
        FROM orders
        WHERE status='Menunggu Pembayaran'
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


def get_paid_orders():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            invoice,
            username,
            layanan,
            harga,
            status
        FROM orders
        WHERE status='Lunas'
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


def get_rejected_orders():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            invoice,
            username,
            layanan,
            harga,
            status
        FROM orders
        WHERE status='Ditolak'
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


# ==========================
# VERIFIKASI
# ==========================

def update_order_status(invoice, status):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE orders SET status=? WHERE invoice=?",
        (status, invoice)
    )

    conn.commit()
    conn.close()


def get_order(invoice):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            invoice,
            user_id,
            username,
            layanan,
            harga,
            status
        FROM orders
        WHERE invoice=?
    """, (invoice,))

    data = cursor.fetchone()

    conn.close()

    return data


# ==========================
# RIWAYAT ORDER USER
# ==========================

def get_user_orders(user_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            invoice,
            layanan,
            harga,
            status
        FROM orders
        WHERE user_id=?
        ORDER BY id DESC
    """, (user_id,))

    data = cursor.fetchall()

    conn.close()

    return data