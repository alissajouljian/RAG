#rag_pipline.py
import os
import logging
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from online_lookup import online_search
from langchain.embeddings.base import Embeddings
from sentence_transformers import SentenceTransformer

# ------------------------------
# Configure logging
# ------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

VECTOR_DB_DIR = "chroma_db"

# ------------------------------
# Local Embedding Class
# Uses SentenceTransformer for offline embedding
# Can be replaced with OpenAIEmbeddings if needed
# embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
# ------------------------------
class LocalEmbedding(Embeddings):
    def __init__(self):
        self.model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L3-v2")

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self.model.encode(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self.model.encode([text])[0]

# Instantiate embeddings
embedding_local = LocalEmbedding()

# ------------------------------
# Language Model (LLM) for answer generation
# ------------------------------
llm_gpt = ChatOpenAI(
    model_name="gpt-3.5-turbo-16k",
    temperature=0.3,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# ------------------------------
# Initialize Chroma vector DB
# ------------------------------
if os.path.exists(VECTOR_DB_DIR) and os.listdir(VECTOR_DB_DIR):
    vectordb = Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=embedding_local)
    print("Loaded existing vector database.")
else:
    vectordb = Chroma.from_documents([], embedding=embedding_local, persist_directory=VECTOR_DB_DIR)

retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 5})

# ------------------------------
# RetrievalQA chain
# ------------------------------
qa_chain = RetrievalQA.from_chain_type(llm=llm_gpt, retriever=retriever)

# ------------------------------
# Senior-level: Robust answer function
# Handles local retrieval first, then online search fallback
# ------------------------------
def answer_question(query: str) -> str | None:
    try:
        answer = qa_chain.invoke(query)

        # Normalize answer to string
        if isinstance(answer, dict):
            answer_text = answer.get("result", "")
        else:
            answer_text = str(answer)

        # Fallback to online search if local DB has no meaningful result
        if not answer_text.strip():
            logger.info("No local answer found. Using online search.")
            return online_search(query)

        return answer_text

    except Exception as e:
        logger.error(f"Error in RAG pipeline: {e}")
        return online_search(query)
