import os
from fastapi import APIRouter, UploadFile, File

from app.agents.graph import run_ap_workflow
from app.agents.extractor_agent import extract_invoice_data

router = APIRouter()

# Folder where uploaded invoices are stored
UPLOAD_DIR = "data/uploaded_invoices"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload-invoice/")
async def upload_invoice(file: UploadFile = File(...)):
    """
    Upload Invoice PDF → Extract Fields → Run AI AP Workflow
    """

    # ✅ Step 1: Save uploaded PDF locally
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # ✅ Step 2: Extract invoice fields from PDF
    extracted_fields = extract_invoice_data(file_path)

    # ✅ Step 3: Prepare invoice data for workflow
    invoice_data = {
        "vendor": extracted_fields["vendor"],
        "amount": extracted_fields["amount"],
        "invoice_number": extracted_fields["invoice_number"],
        "po_number": extracted_fields["po_number"],
        "vat_number": extracted_fields["vat_number"],
        "scenario": "normal"
    }

    # =========================================================
    # ✅ TEMPORARY VAT TEST PATCH
    # Force PO number so VAT failure rule can trigger properly
    # Remove this later when real PO extraction is implemented
    # =========================================================
    invoice_data["po_number"] = "PO-TEST-001"

    # ✅ Step 4: Run Autonomous AP Workflow
    workflow_result = run_ap_workflow(invoice_data)

    # ✅ Step 5: Return response JSON
    return {
        "message": "✅ Invoice processed successfully",
        "uploaded_file": file.filename,
        "extracted_fields": extracted_fields,
        "workflow_invoice_data": invoice_data,
        "workflow_result": workflow_result
    }
