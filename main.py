#main.py
import os
import logging
import warnings
from dotenv import load_dotenv



# add document: test_docs/text1.txt
# search: when is the Coldboy concert?


# ------------------------------
# Suppress warnings for clean logging
# ------------------------------
warnings.filterwarnings("ignore")
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GRPC_GO_LOG_SEVERITY_LEVEL"] = "ERROR"
os.environ["CHROMA_LOG_LEVEL"] = "ERROR"
os.environ["CHROMA_ENABLE_TELEMETRY"] = "False"

logging.getLogger("sentence_transformers").setLevel(logging.WARNING)
logging.getLogger("transformers").setLevel(logging.WARNING)

# ------------------------------
# Load environment variables
# ------------------------------
load_dotenv()

# ------------------------------
# Import project modules
# ------------------------------
from ingestion import ingest_document
from rag_pipeline import answer_question
from online_lookup import online_search

# ------------------------------
# CLI interface for senior-level RAG pipeline
# ------------------------------
def main():
    print("Welcome to the Concert Tour Bot!")

    while True:
        user_input = input("\nType your command (or 'exit'): ").strip()
        if user_input.lower() == 'exit':
            break

        if user_input.lower().startswith("add document:"):
            path = user_input[len("add document:"):].strip()
            if not os.path.exists(path):
                print("Document not found.")
                continue

            with open(path, "rb") as f:
                file_bytes = f.read()

            summary = ingest_document(file_bytes, os.path.basename(path))
            print(f"\nDocument Summary:\n{summary}")

        elif user_input.lower().startswith("search:"):
            query = user_input[len("search:"):].strip()
            answer = answer_question(query)
            if answer:
                print(f"\nAnswer: {answer}")
            else:
                print("\nNo local info found. Searching online...")
                web_answer = online_search(query)
                print(f"\nOnline Result: {web_answer}")

        else:
            print("Unknown command. Use 'add document: [path]' or 'search: [query]'")

if __name__ == "__main__":
    main()
