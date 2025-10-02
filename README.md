Absolutely! I will write a **very detailed, step-by-step README** for your project, assuming a beginner can follow it, while still being comprehensive for a senior-level ML engineer like yourself. I’ll also explain how to use **Poetry (`pyproject.toml`)**, run the code, add documents, search, and finally push to GitHub.

Here’s a full README:

---

# 🎵 Concert Tour Helper (RAG Pipeline)

A **senior-level Retrieval-Augmented Generation (RAG) application** to manage concert tour documents and answer questions using a combination of **local embeddings** and **online search**. Built using **LangChain**, **Chroma vector database**, **Sentence Transformers**, **OpenAI GPT**, and **Google Gemini LLM**.

This project allows you to:

1. Add concert documents (txt, pdf, docx, csv, json) and summarize them.
2. Ask questions about concerts and get answers from local data or online search.
3. Search artists online directly with structured JSON responses.
4. Use both CLI and Streamlit web interface.

---

## **Table of Contents**

1. [Project Setup](#project-setup)
2. [Environment Variables](#environment-variables)
3. [Install Dependencies](#install-dependencies)
4. [Running the CLI](#running-the-cli)
5. [Running the Streamlit App](#running-the-streamlit-app)
6. [Adding Documents](#adding-documents)
7. [Searching Questions](#searching-questions)
8. [Project Structure](#project-structure)
9. [Git Setup & Push](#git-setup--push)
10. [Notes](#notes)

---

## **Project Setup**

1. Clone the repository:

```bash
git clone <your-repo-url>
cd <your-repo-name>
```

2. Make sure you have **Python 3.11+** installed.

3. Create a `.env` file in the root folder with the following keys:

```
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_google_gemini_key_here
SERPAPI_API_KEY=your_serpapi_key_here
```

> **Important:** This file contains sensitive API keys. Do **not** commit it to GitHub.

4. You already have `pyproject.toml` (Poetry project). Use it to install dependencies:

```bash
# Install Poetry if not already installed
pip install poetry

# Install dependencies from pyproject.toml
poetry install

# Activate virtual environment
poetry shell
```

---

## **Running the CLI**

After activating the Poetry shell:

```bash
python main.py
```

You will see:

```
Welcome to the Concert Tour Bot!
```

You can now type commands.

---

### **Commands**

1. **Add a document**:

```
add document: path/to/your/document.txt
```

* Supported formats: `.txt`, `.pdf`, `.docx`, `.json`, `.csv`.
* The system will:

  * Extract text
  * Check if the content is concert-related
  * Summarize it using Google Gemini LLM
  * Save it to **Chroma vector database**
  * Update `reports/report.json` with summary info

**Example:**

```
add document: test_docs/text1.txt
```

---

2. **Search / Ask a question**:

```
search: when is the Coldboy concert?
```

* The system will first check **local database** for answers.
* If no answer found, it uses **online search** and Gemini LLM to give structured results.
* Returns either a text answer or a JSON object with artist, date, venue, summary.

**Example:**

```
search: When is Taylor Swift's next concert in Europe?
```

---

3. **Exit CLI**:

```
exit
```

---

## **Running the Streamlit App**

Streamlit provides a web interface to do the same things:

```bash
streamlit run streamlit_app.py
```

* Modes:

  1. **Ask a question** – input query and get answers.
  2. **Add a document** – upload file directly.
  3. **Search artist online** – structured JSON search.

---

## **Adding Documents (Step-by-Step)**

1. Prepare your document file (`.txt`, `.pdf`, `.docx`, `.json`, `.csv`) containing concert/tour info.
2. Either:

   * Use CLI command: `add document: path/to/file.txt`
   * Or upload via Streamlit app.
3. System will extract, summarize, and store in **local vector database**.
4. You will get a **confirmation message** with a summary.

---

## **Searching Questions (Step-by-Step)**

1. Use CLI:

```bash
search: [your question here]
```

2. Or in Streamlit:

   * Select **Ask a question**
   * Enter query
   * Submit
3. Answer returned from:

   * Local Chroma vector DB (first)
   * Online search + Gemini LLM (fallback)

---

## **Project Structure**

```
concert-tour-helper/
│
├─ main.py                  # CLI entrypoint
├─ streamlit_app.py         # Streamlit web app
├─ rag_pipeline.py          # RAG pipeline (embedding, vector DB, LLM)
├─ ingestion.py             # Document ingestion and summarization
├─ online_lookup.py         # Online search wrapper with Gemini + SERP API
├─ utils/
│  ├─ doc_loader.py         # Load txt, pdf, docx
│  └─ summarizer.py         # Summarize document with Gemini LLM
├─ chroma_db/               # Local vector DB (auto-generated)
├─ reports/
│  └─ report.json           # Document ingestion reports
├─ pyproject.toml           # Poetry project config
└─ .env                     # API keys (not in repo)
```
