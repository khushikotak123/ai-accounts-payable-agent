import sqlite3
from datetime import datetime, timedelta

DB_PATH = "data/ap.db"


def check_sla_breaches():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT invoice_number, due_date, sla_warned
    FROM invoices
    WHERE status = 'PENDING'
      AND due_date IS NOT NULL
    """)

    rows = cursor.fetchall()
    now = datetime.utcnow()

    for invoice_number, due_date_str, sla_warned in rows:
        try:
            due_date = datetime.fromisoformat(due_date_str)
        except Exception:
            continue

        # Warn only once and only if due within 48 hours
        if (
            due_date > now and
            due_date - now <= timedelta(days=2) and
            sla_warned == 0
        ):
            print(
                f"⚠️ SLA RISK: Invoice {invoice_number} due soon "
                f"({due_date.isoformat()})"
            )

            cursor.execute("""
            UPDATE invoices
            SET sla_warned = 1
            WHERE invoice_number = ?
            """, (invoice_number,))

    conn.commit()
    conn.close()
