from ingestion import ingest_document
from rag_pipeline import answer_question
from online_lookup import online_search
import os

def main():
    print("Welcome to the Concert Tour Bot!")
    while True:
        user_input = input("\nType your command (or 'exit'): ")

        if user_input.lower() == 'exit':
            break

        if user_input.lower().startswith("add document: "):
            doc_path = user_input[len("add document: "):].strip()
            if not os.path.exists(doc_path):
                print("Document not found.")
                continue
            summary = ingest_document(doc_path)
            print(f"\nThank you! Here is a summary of the document:\n{summary}")

        elif user_input.lower().startswith("search: "):
            query = user_input[len("search: "):].strip()
            print("\nSearching the ingested documents...")
            answer = answer_question(query)
            if answer:
                print(f"\nAnswer: {answer}")
            else:
                print("\nNo relevant information found in local documents. Performing online search...")
                web_answer = online_search(query)
                print(f"\nOnline Result: {web_answer}")

        else:
            print("Unknown command. Please use 'add document: [path]' or 'search: [query]'")


if __name__ == '__main__':
    main()
