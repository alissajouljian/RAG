# ingestion.py
import os
import json
import tempfile
import logging
import pandas as pd
import re
from dotenv import load_dotenv
from rag_pipeline import vectordb
from utils.doc_loader import load_document
from utils.summarizer import summarize_text
from langchain_core.documents import Document

# ------------------------------
# Load environment variables
# ------------------------------
load_dotenv()

# ------------------------------
# Logging setup
# ------------------------------
logger = logging.getLogger(__name__)

# ------------------------------
# Constants
# ------------------------------
REPORT_PATH = os.path.join("reports", "report.json")

CONCERT_KEYWORDS = [
    "concert", "tour", "venue", "performance", "show", "tickets", "album", "dates",
    "venues", "special guest", "live", "gig", "headliner", "support act", "festival",
    "tour dates", "pre-sale", "on sale", "ticketmaster", "event", "location", "stadium",
    "arena", "amphitheatre", "sold out", "setlist", "world tour", "europe tour",
    "north america", "touring", "music tour"
]

# ------------------------------
# Helper Functions
# ------------------------------
def is_concert_related(text: str) -> bool:
    """Check if the text mentions concerts or tours."""
    return any(keyword in text.lower() for keyword in CONCERT_KEYWORDS)

# ------------------------------
# Main ingestion function
# ------------------------------
def ingest_document(file_content: bytes, filename: str) -> str | dict:
    """
    Ingest a document, generate a summary, and add it to the vector DB.

    Supports .txt, .pdf, .docx, .json, .csv formats.
    """

    # Save uploaded file temporarily
    suffix = os.path.splitext(filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(file_content)
        tmp_path = tmp_file.name

    # Load raw text from file
    ext = suffix.lower()
    if ext in [".txt", ".pdf", ".docx"]:
        raw_text = load_document(tmp_path)
    elif ext == ".json":
        with open(tmp_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            raw_text = " ".join(str(v) for v in data.values())
    elif ext == ".csv":
        df = pd.read_csv(tmp_path)
        raw_text = " ".join(df.astype(str).values.flatten())
    else:
        logger.warning(f"Unsupported file format: {ext}")
        return f"Unsupported file format: {ext}"

    # Check if the document is concert-related
    if not is_concert_related(raw_text):
        return "Sorry, I cannot ingest documents with other themes."

    # Summarize document
    summary = summarize_text(raw_text)
    if not isinstance(summary, str):
        return "Failed to generate a valid summary for the document."

    # Extract metadata
    metadata = {"source": filename}
    artist_match = re.search(r"artist[:\s]*(\w+)", raw_text, re.IGNORECASE)
    date_match = re.search(r"date[:\s]*(\d{4}-\d{2}-\d{2})", raw_text)
    venue_match = re.search(r"venue[:\s]*(.*)", raw_text)

    if artist_match: metadata["artist"] = artist_match.group(1)
    if date_match: metadata["date"] = date_match.group(1)
    if venue_match: metadata["venue"] = venue_match.group(1)

    # Create document and add to vector DB
    doc = Document(page_content=summary, metadata=metadata)
    vectordb.add_documents([doc])

    # Save ingestion report
    os.makedirs("reports", exist_ok=True)
    report_data = []
    if os.path.exists(REPORT_PATH):
        with open(REPORT_PATH, "r") as f:
            report_data = json.load(f)
    report_data.append({"file": filename, "summary": summary})
    with open(REPORT_PATH, "w") as f:
        json.dump(report_data, f, indent=2)

    return summary
