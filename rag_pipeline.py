from dotenv import load_dotenv
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAI
import os

load_dotenv()

VECTOR_DIR = "vector_store"


embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=os.getenv("GEMINI_API_KEY"))

llm = GoogleGenerativeAI(model="gemini-1.5-pro", api_key=os.getenv("GEMINI_API_KEY"), temperature=0.3)

if os.path.exists(VECTOR_DIR):
    vectordb = Chroma(
        persist_directory=VECTOR_DIR,
        embedding_function=embedding,
        collection_metadata={"hnsw:space": "cosine"}
    )
else:
    vectordb = Chroma.from_documents(
        documents=[],
        embedding=embedding,
        persist_directory=VECTOR_DIR,
        collection_metadata={"hnsw:space": "cosine"}
    )

retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 5})
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

def ingest_to_vectorstore(docs: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = text_splitter.split_documents(docs)
    vectordb.add_documents(split_docs)
    vectordb.persist()
    print(f"Ingested {len(split_docs)} chunks into vector store.")

def answer_question(query: str):
    return qa_chain.run(query)
