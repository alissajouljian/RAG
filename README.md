
#  Concert Tour Helper

**Concert Tour Helper** is a Retrieval-Augmented Generation (RAG) assistant built with LangChain, ChromaDB, and LLM APIs (Gemini, OpenAI) to analyze, summarize, and answer questions about 2025–2026 concert tour documents. Users can upload various document formats, receive structured summaries, ask tour-related questions, and optionally retrieve answers from the web using SerpAPI. The project includes both CLI and a user-friendly Streamlit interface.

---

##  Project Structure

```
concert-tour-helper/
├── .env                     # Configuration file storing API keys
├── main.py                  # CLI entry point for ingestion and Q&A
├── config.py 
├── streamlit_app.py         # Streamlit UI entry point
├── ingestion.py             # Handles file loading, validation, and vector storage
├── rag_pipeline.py          # Core RAG logic: retrieval, similarity, LLM answering
├── online_lookup.py         # Web fallback using SerpAPI and Gemini
├── utils/
│   ├── doc_loader.py        # Loads and extracts text from TXT, PDF, DOCX
│   └── summarizer.py        # Uses Gemini to summarize tour info
├── reports/
│   └── report.json          # Stores generated document summaries
├── vector_store/            # ChromaDB persistent storage
├── requirements.txt         # List of required Python packages
└── README.md                # This file
```

---

##  Requirements

Install all dependencies using:

```bash
pip install -r requirements.txt
```

>  You must also set up the `.env` file with your API keys before running the application.

---

## Running the Project

### Option 1: Run with Streamlit UI

```bash
streamlit run streamlit_app.py
```

This launches a web interface where you can:
- Upload and summarize concert tour documents.
- Ask questions about stored tours using RAG.
- Fall back to online search if needed.

### Option 2: Use Command Line (CLI)

```bash
python main.py
```

When running via CLI:
1. You’ll be prompted to input the file path for document ingestion.
2. Summaries are stored in `reports/report.json`.
3. You can then ask questions which will be answered using document embeddings or via online lookup.

---

##  How It Works

1. **Document Ingestion**  
   Files (.txt ) are parsed, checked for concert-related content, and summarized using Gemini. Embeddings are stored in ChromaDB.

2. **Question Answering (RAG)**  
   The system retrieves relevant chunks from the vector store and uses Gemini or OpenAI to generate accurate, grounded answers.

3. **Online Search Fallback**  
   If no relevant documents are found, SerpAPI is used to pull search results, which are summarized with Gemini.

---

##  Summarized Data Format

The system produces structured summaries with:
- Artist name(s)
- Tour name or theme
- Tour locations (cities, venues)
- Tour dates
- Ticket sale or presale dates
- Supporting acts
- Notable news (e.g., cancellations, changes)

Stored in JSON at `reports/report.json`.


