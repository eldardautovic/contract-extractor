from fastapi import UploadFile
from pypdf import PdfReader


def extract_text_from_pdf(file: UploadFile):  
    text = ""
    try:
        reader = PdfReader(file.file)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        print(f"Greška pri čitanju PDF-a: {e}")
    return text

