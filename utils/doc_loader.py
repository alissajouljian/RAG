import os
from PyPDF2 import PdfReader
from docx import Document as DocxDocument

def load_document(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()

    if ext == ".txt":
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    elif ext == ".pdf":
        reader = PdfReader(path)
        return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

    elif ext == ".docx":
        doc = DocxDocument(path)
        return "\n".join(para.text for para in doc.paragraphs)

    else:
        raise ValueError("Unsupported file format")
