import pytesseract
from PIL import Image
import fitz


def extract_text_from_file(file_path):
    text = ""

    if file_path.lower().endswith(".pdf"):
        pdf = fitz.open(file_path)
        for page in pdf:
            text += page.get_text()
    else:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)

    return text