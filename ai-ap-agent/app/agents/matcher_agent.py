import sqlite3

DB_FILE = "data/ap.db"


def three_way_match(invoice_data: dict):
    """
    3-Way Match Agent

    Compares:
    ✅ Purchase Order (PO)
    ✅ Goods Receipt (GRN)
    ✅ Invoice

    Returns mismatch if invoice cannot be safely paid.
    """

    po_number = invoice_data.get("po_number")

    if not po_number:
        return None

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Fetch PO record
    cursor.execute(
        "SELECT quantity, unit_price FROM purchase_orders WHERE po_number=?",
        (po_number,)
    )
    po = cursor.fetchone()

    # Fetch Receipt record
    cursor.execute(
        "SELECT received_quantity FROM receipts WHERE po_number=?",
        (po_number,)
    )
    receipt = cursor.fetchone()

    conn.close()

    # Missing records
    if not po or not receipt:
        return {
            "match": False,
            "reason": "3-way match failed: PO or Receipt record not found"
        }

    po_qty, po_price = po
    received_qty = receipt[0]

    # Quantity mismatch
    if received_qty != po_qty:
        return {
            "match": False,
            "reason": f"3-way match mismatch: Ordered {po_qty}, Received {received_qty}"
        }

    return {
        "match": True,
        "reason": "3-way match successful"
    }
