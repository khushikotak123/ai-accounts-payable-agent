import pdfplumber


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from PDF (works if PDF has selectable text)
    """
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

    return text
