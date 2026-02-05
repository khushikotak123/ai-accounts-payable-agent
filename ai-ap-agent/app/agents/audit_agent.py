from datetime import datetime


def log_audit(event: str, invoice: dict, decision: dict):
    """
    Simple audit logger (DB later).
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": event,
        "invoice_number": invoice.get("invoice_number"),
        "status": decision.get("status"),
        "reason": decision.get("reason"),
        "policies_used": decision.get("policy_sources"),
    }

    print("\n📋 AUDIT LOG")
    print(log_entry)

    return log_entry
