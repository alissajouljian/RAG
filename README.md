
# Concert Tour Helper Project

This project implements a **Retrieval-Augmented Generation (RAG) pipeline** for managing and querying concert tour documents. It uses **LangChain**, **Chroma vector database**, **Sentence Transformers**, **OpenAI GPT**, and **Google Gemini LLM** to extract, summarize, and answer questions about concert tours.

The system allows you to:

* Add concert documents (`.txt`, `.pdf`, `.docx`, `.csv`, `.json`) and generate summaries.
* Ask questions about concerts and receive answers from **local data** or **online search**.
* Search artists online directly with **structured JSON responses**.
* Use both **CLI** and **Streamlit web interface**.

---

## Project Structure

```
concert-tour-helper/
├─ main.py                  # CLI entrypoint
├─ streamlit_app.py         # Streamlit web app
├─ rag_pipeline.py          # RAG pipeline (embedding, vector DB, LLM)
├─ ingestion.py             # Document ingestion and summarization
├─ online_lookup.py         # Online search wrapper with Gemini + SERP API
├─ utils/
│  ├─ doc_loader.py         # Load txt, pdf, docx documents
│  └─ summarizer.py         # Summarize document with Gemini LLM
├─ chroma_db/               # Local vector DB (auto-generated)
├─ reports/
│  └─ report.json           # Document ingestion reports
├─ pyproject.toml           # Poetry project config
└─ .env                     # API keys (not in repo)
```

---

## Requirements

Install all necessary dependencies using **Poetry**:

```bash
# Install Poetry if not installed
pip install poetry

# Install dependencies from pyproject.toml
poetry install

# Activate virtual environment
poetry shell
```

### Environment Variables

Create a `.env` file in the root directory with the following keys:

```
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_google_gemini_key_here
SERPAPI_API_KEY=your_serpapi_key_here
```

> ⚠️ Important: `.env` contains sensitive API keys. Do **not** commit it to GitHub.

---

## Running the CLI

Activate the Poetry shell and run:

```bash
python main.py
```

You will see:

```
Welcome to the Concert Tour Bot!
You can now type commands.
```

### Commands

**1. Add a document**

```bash
add document: path/to/your/document.txt
```

Supported formats: `.txt`, `.pdf`, `.docx`, `.json`, `.csv`.

The system will:

* Extract text from the document.
* Verify if the content is concert-related.
* Summarize it using **Google Gemini LLM**.
* Store it in the **Chroma vector database**.
* Update `reports/report.json` with the summary.

Example:

```bash
add document: test_docs/text1.txt
```

---

**2. Search / Ask a question**

```bash
search: when is the Coldboy concert?
```

The system will:

1. First check the **local vector database**.
2. If no result is found, fallback to **online search + Gemini LLM**.

Returns either a **text answer** or a **JSON object** containing:

* Artist
* Tour date
* Venue
* Short summary

Example:

```bash
search: When is Taylor Swift's next concert in Europe?
```

---

**3. Exit CLI**

```bash
exit
```

---

## Running the Streamlit Web App

Run the Streamlit interface:

```bash
streamlit run streamlit_app.py
```

### Modes

1. **Ask a question** – Input query and get answers from local or online sources.
2. **Add a document** – Upload a file directly.
3. **Search artist online** – Perform structured JSON search for any artist.

---

## Adding Documents (Step-by-Step)

1. Prepare your document file (`.txt`, `.pdf`, `.docx`, `.json`, `.csv`) containing concert or tour information.
2. Use either the **CLI** or **Streamlit upload**.
3. The system will automatically extract, summarize, and store the document in **ChromaDB**.
4. You will receive a **confirmation message** with a concise summary.

---

## Searching Questions (Step-by-Step)

1. Use the **CLI** or **Streamlit "Ask a question" mode**.
2. Enter your query.
3. The system retrieves answers from **local Chroma DB** first, then **online search** if needed.

---

## Optimization Ideas

* **Chunking Parameters**: Experiment with chunk sizes and overlap for better context.
* **Embedding Models**: Compare OpenAI embeddings vs local SentenceTransformer models.
* **Retrieval Tuning**: Adjust similarity thresholds and number of retrieved chunks.
* **Prompt Engineering**: Refine prompts for more accurate summaries and answers.
* **Model Ensemble**: Combine multiple LLMs for robust results.
* **Monitoring**: Track token usage, latency, and performance metrics with LangSmith or custom tools.

---

## Contributing

Contributions and suggestions are welcome! Open issues or submit pull requests.
