from app.agents.validator_agent import validate_invoice

# Test invoice scenario
invoice = {
    "vendor": "ABC Ltd",
    "amount": 2400,
    "invoice_number": "INV-1291",
    "scenario": "normal"
}

result = validate_invoice(invoice)

print("\n✅ VALIDATION RESULT\n")
print(result)

# Fraud scenario
fraud_invoice = {
    "vendor": "XYZ Corp",
    "amount": 500,
    "invoice_number": "INV-2001",
    "scenario": "bank_change"
}

fraud_result = validate_invoice(fraud_invoice)

print("\n🚨 FRAUD VALIDATION RESULT\n")
print(fraud_result)
