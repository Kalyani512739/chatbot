import fitz
import re

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        page_text = page.get_text("text")

        # remove extra spaces/newlines
        page_text = re.sub(r'\n+', '\n', page_text)
        page_text = re.sub(r'\s+', ' ', page_text)

        text += page_text + "\n"

    return text