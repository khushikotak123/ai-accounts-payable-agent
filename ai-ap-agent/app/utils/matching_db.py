import sqlite3

DB_FILE = "data/ap.db"


def init_matching_tables():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Purchase Orders
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS purchase_orders (
        po_number TEXT PRIMARY KEY,
        item TEXT,
        quantity INTEGER,
        unit_price REAL
    )
    """)

    # Goods Receipts
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS receipts (
        receipt_id INTEGER PRIMARY KEY AUTOINCREMENT,
        po_number TEXT,
        received_quantity INTEGER
    )
    """)

    conn.commit()
    conn.close()


def seed_demo_po():
    """
    Add one demo PO for testing
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO purchase_orders
    (po_number, item, quantity, unit_price)
    VALUES (?, ?, ?, ?)
    """, ("PO-TEST-001", "Cosmetic Item", 10, 20.0))

    cursor.execute("""
    INSERT OR REPLACE INTO receipts
    (po_number, received_quantity)
    VALUES (?, ?)
    """, ("PO-TEST-001", 8))

    conn.commit()
    conn.close()
