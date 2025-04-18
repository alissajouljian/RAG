import os
import json
import tempfile
from langchain_core.documents import Document
from utils.doc_loader import load_document
from utils.summarizer import summarize_text
from rag_pipeline import ingest_to_vectorstore

REPORT_PATH = os.path.join("reports", "report.json")

def is_concert_related(document_text):
    keywords = [
        "concert", "tour", "venue", "performance", "show", "tickets", "album", "dates", "venues", "special guest",
        "live", "gig", "headliner", "support act", "festival", "tour dates", "pre-sale", "on sale", 
        "ticketmaster", "event", "location", "stadium", "arena", "amphitheatre", "sold out", 
        "setlist", "world tour", "europe tour", "north america", "touring", "music tour"
    ]
    return any(keyword in document_text.lower() for keyword in keywords)

def ingest_document(file_content: bytes, filename: str):
    suffix = os.path.splitext(filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(file_content)
        tmp_path = tmp_file.name

    raw_text = load_document(tmp_path)

    if not is_concert_related(raw_text):
        return "Sorry, I cannot ingest documents with other themes."

    summary = summarize_text(raw_text)
    if not isinstance(summary, str):
        return "Failed to generate a valid summary for the document."

    metadata = {"source": filename}
    doc = Document(page_content=summary, metadata=metadata)

    ingest_to_vectorstore([doc])

    os.makedirs("reports", exist_ok=True)
    report_data = []
    if os.path.exists(REPORT_PATH):
        with open(REPORT_PATH, "r") as f:
            report_data = json.load(f)

    report_data.append({"file": filename, "summary": summary})

    with open(REPORT_PATH, "w") as f:
        json.dump(report_data, f, indent=2)

    return summary
