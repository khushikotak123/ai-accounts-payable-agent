from datetime import datetime, timedelta

from app.rag.retriever import retrieve_policy
from app.utils.duplicate_check import init_db, is_duplicate, save_invoice

from app.agents.matcher_agent import three_way_match
from app.utils.matching_db import init_matching_tables, seed_demo_po


# ✅ Initialize databases once
init_db()
init_matching_tables()

# ✅ Seed demo PO + Receipt for mismatch testing
seed_demo_po()


def validate_invoice(invoice_data: dict):
    """
    Validator Agent (Offline + Policy Grounded)

    Covers:
    ✅ Duplicate Invoice Detection
    ✅ Missing PO Exception Workflow
    ✅ 3-Way Match Mismatch Escalation
    ✅ VAT Validation Failure Blocking
    ✅ Fraud Guardrails
    ✅ Approval Threshold Routing
    ✅ SLA Due Date Simulation (NEW Step 12E)
    """

    invoice_number = invoice_data.get("invoice_number", "UNKNOWN")
    amount = invoice_data.get("amount", 0)

    # =====================================================
    # ✅ Step 1: Duplicate Invoice Check
    # =====================================================
    if is_duplicate(invoice_number):
        return {
            "status": "REJECTED",
            "reason": f"Duplicate invoice detected for invoice_number={invoice_number}. Payment blocked.",
            "policy_sources": ["fraud_controls.txt"]
        }

    # =====================================================
    # ✅ Step 2: SLA Due Date Simulation (NEW)
    # Every invoice is due in 1 day for demo purposes
    # =====================================================
    due_date = (datetime.utcnow() + timedelta(days=1)).isoformat()

    # ✅ Save invoice into DB as PENDING for SLA monitoring
    save_invoice(
        vendor=invoice_data.get("vendor", "UNKNOWN"),
        invoice_number=invoice_number,
        amount=amount,
        due_date=due_date
    )

    # =====================================================
    # ✅ Step 3: Missing PO Exception Handling
    # =====================================================
    if invoice_data.get("po_number") is None:
        return {
            "status": "ESCALATE",
            "reason": "Missing Purchase Order. Routed to exception approval workflow.",
            "policy_sources": ["approval_policy.txt"]
        }

    # =====================================================
    # ✅ Step 4: 3-Way Match Validation (Invoice vs PO vs Receipt)
    # =====================================================
    match_result = three_way_match(invoice_data)

    if match_result and match_result["match"] is False:
        return {
            "status": "ESCALATE",
            "reason": match_result["reason"],
            "policy_sources": ["invoice_guidelines.txt"]
        }

    # =====================================================
    # ✅ Step 5: VAT Validation Failure Enforcement
    # =====================================================
    if invoice_data.get("vat_number") is None:
        return {
            "status": "REJECTED",
            "reason": "VAT validation failed. Missing VAT/GST number. Payment blocked.",
            "policy_sources": ["vat_rules.txt"]
        }

    # =====================================================
    # ✅ Step 6: Retrieve Policies via RAG
    # =====================================================
    query = f"""
    Validate invoice:
    vendor={invoice_data.get("vendor")}
    amount={amount}
    scenario={invoice_data.get("scenario")}
    """

    policies = retrieve_policy(query, top_k=2)

    # ✅ Default Decision
    decision = {
        "status": "APPROVED",
        "reason": "Invoice is valid under policy.",
        "policy_sources": [p["source"] for p in policies]
    }

    # =====================================================
    # ✅ Step 7: Fraud Guardrail (Bank Detail Change)
    # =====================================================
    if invoice_data.get("scenario") == "bank_change":
        decision["status"] = "ESCALATE"
        decision["reason"] = "Bank detail change requires human verification."

    # =====================================================
    # ✅ Step 8: Approval Threshold Guardrail
    # =====================================================
    elif amount > 1000:
        decision["status"] = "ESCALATE"
        decision["reason"] = "Invoice exceeds auto-approval threshold (£1000)."

    return decision
