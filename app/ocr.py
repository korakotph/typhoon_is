import pytesseract
from PIL import Image


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

def extract_text(path: str):
    img = Image.open(path)
    text = pytesseract.image_to_string(img, lang="tha+eng")

    text = text.strip()

    return {
        "text": text,
        "char_count": len(text),
        "word_count": len(text.split())
    }
