from app.agents.graph import run_ap_workflow

invoice = {
    "vendor": "ABC Ltd",
    "amount": 2400,
    "invoice_number": "INV-1291",
    "scenario": "normal"
}

result = run_ap_workflow(invoice)

print("\n🧠 FINAL WORKFLOW STATE\n")
print(result)
