import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Tabel pengguna
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    coin INTEGER DEFAULT 0
)
""")

# Tabel pesanan
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    promo_text TEXT,
    package TEXT,
    price INTEGER,
    status TEXT DEFAULT 'Menunggu Pembayaran',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()
