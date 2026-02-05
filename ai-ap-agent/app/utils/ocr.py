import pytesseract
from PIL import Image


def extract_text_from_image(image: Image.Image) -> str:
    """
    Extract text from scanned image using Tesseract OCR
    """
    return pytesseract.image_to_string(image)
