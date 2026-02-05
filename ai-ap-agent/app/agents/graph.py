from typing import TypedDict, Optional

from langgraph.graph import StateGraph

from app.agents.validator_agent import validate_invoice
from app.agents.audit_agent import log_audit


# ✅ Correct LangGraph State Schema
class InvoiceState(TypedDict):
    invoice: dict
    decision: Optional[dict]
    approval: Optional[str]


def run_ap_workflow(invoice: dict):

    graph = StateGraph(InvoiceState)

    # --- Node 1: Validate ---
    def validate(state: InvoiceState):
        decision = validate_invoice(state["invoice"])
        return {"decision": decision}

    # --- Node 2: Route Approval ---
    def route_approval(state: InvoiceState):
        decision = state["decision"]

        if decision["status"] == "ESCALATE":
            approval = "HUMAN_REQUIRED"

        elif decision["status"] == "REJECTED":
            approval = "PAYMENT_BLOCKED"

        else:
            approval = "AUTO_APPROVED"

        return {"approval": approval}

    # --- Node 3: Audit Log ---
    def audit(state: InvoiceState):
        log_audit(
            event="INVOICE_PROCESSED",
            invoice=state["invoice"],
            decision=state["decision"],
        )
        return {}

    # ✅ Register nodes
    graph.add_node("validate", validate)
    graph.add_node("route_approval", route_approval)
    graph.add_node("audit", audit)

    # ✅ Graph flow
    graph.set_entry_point("validate")
    graph.add_edge("validate", "route_approval")
    graph.add_edge("route_approval", "audit")

    workflow = graph.compile()

    # ✅ Invoke with proper schema
    return workflow.invoke({"invoice": invoice})
