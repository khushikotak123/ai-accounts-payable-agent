import re
from app.utils.pdf_reader import extract_text_from_pdf


def extract_invoice_data(pdf_path: str) -> dict:
    """
    General Invoice Extractor (Multi-Format)

    Extracts:
    ✅ Invoice Number
    ✅ Total Amount (Robust)
    ✅ PO Number
    ✅ VAT/GST Number
    """

    raw_text = extract_text_from_pdf(pdf_path)

    # -------------------------------------------------
    # ✅ Invoice Number Extraction (multi-format)
    # -------------------------------------------------
    invoice_patterns = [
        r"Invoice Number\s*:\s*([A-Z0-9-]+)",
        r"Invoice No\.?\s*:\s*([A-Z0-9-]+)",
        r"Invoice\s*#\s*:\s*([A-Z0-9-]+)"
    ]

    invoice_number = "UNKNOWN"
    for pattern in invoice_patterns:
        match = re.search(pattern, raw_text, re.IGNORECASE)
        if match:
            invoice_number = match.group(1)
            break

    # -------------------------------------------------
    # ✅ Robust Amount Extraction (Enterprise Grade)
    # -------------------------------------------------
    amount = 0.0

    # ✅ 1. Try labelled totals first
    amount_patterns = [
        r"Grand Total\s*[:\-]?\s*₹?\s*([\d,]+\.?\d*)",
        r"Total Amount\s*[:\-]?\s*₹?\s*([\d,]+\.?\d*)",
        r"Invoice Value\s*[:\-]?\s*₹?\s*([\d,]+\.?\d*)",
        r"Net Payable\s*[:\-]?\s*₹?\s*([\d,]+\.?\d*)",
        r"Amount Payable\s*[:\-]?\s*₹?\s*([\d,]+\.?\d*)",
        r"Total\s*[:\-]?\s*₹?\s*([\d,]+\.?\d*)",
        r"TOTAL\s*Rs\.?\s*([\d,]+\.?\d*)",
    ]

    for pattern in amount_patterns:
        match = re.search(pattern, raw_text, re.IGNORECASE)
        if match:
            amount = float(match.group(1).replace(",", ""))
            break

    # ✅ 2. Fallback: Extract all currency-like numbers (₹ or Rs)
    if amount == 0.0:
        all_amounts = re.findall(
            r"(?:₹|Rs\.?)\s*([\d,]+\.?\d*)",
            raw_text
        )

        if all_amounts:
            numeric_amounts = [float(a.replace(",", "")) for a in all_amounts]
            amount = max(numeric_amounts)

    # ✅ 3. Final fallback: pick largest large number (>100)
    if amount == 0.0:
        numbers = re.findall(r"\b\d{3,7}\b", raw_text)
        if numbers:
            numeric_amounts = [float(n) for n in numbers]
            amount = max(numeric_amounts)

    # -------------------------------------------------
    # ✅ PO Number Extraction
    # -------------------------------------------------
    po_match = re.search(
        r"(PO Number|Purchase Order)\s*:?[\s]*([A-Z0-9-]+)",
        raw_text,
        re.IGNORECASE
    )
    po_number = po_match.group(2) if po_match else None

    # -------------------------------------------------
    # ✅ VAT / GST Number Extraction
    # -------------------------------------------------
    vat_match = re.search(
        r"(GST|VAT)\s*(Registration)?\s*(No\.?|Number)?\s*:?[\s]*([A-Z0-9]+)",
        raw_text,
        re.IGNORECASE
    )
    vat_number = vat_match.group(4) if vat_match else None

    return {
        "vendor": "Unknown Vendor (extract next)",
        "invoice_number": invoice_number,
        "amount": amount,
        "po_number": po_number,
        "vat_number": vat_number,
        "raw_text_preview": raw_text[:400]
    }
