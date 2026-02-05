import sqlite3
from datetime import datetime

DB_PATH = "data/ap.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vendor TEXT,
        invoice_number TEXT UNIQUE,
        amount REAL,
        status TEXT DEFAULT 'PENDING',
        due_date TEXT,
        sla_warned INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def is_duplicate(invoice_number: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT 1 FROM invoices WHERE invoice_number = ?",
        (invoice_number,)
    )

    exists = cursor.fetchone() is not None
    conn.close()
    return exists


def save_invoice(vendor, invoice_number, amount, due_date):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO invoices
    (vendor, invoice_number, amount, due_date, status, sla_warned)
    VALUES (?, ?, ?, ?, 'PENDING', 0)
    """, (vendor, invoice_number, amount, due_date))

    conn.commit()
    conn.close()


def update_status(invoice_number, status):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE invoices
    SET status = ?
    WHERE invoice_number = ?
    """, (status, invoice_number))

    conn.commit()
    conn.close()
