# utils/summarizer.py
import os
import logging
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.messages.ai import AIMessage

# ------------------------------
# Load environment variables
# ------------------------------
load_dotenv()
logger = logging.getLogger(__name__)

# ------------------------------
# Gemini LLM for summarization
# ------------------------------
gemini_llm = GoogleGenerativeAI(
    model="gemini-2.5-pro",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.3
)

# ------------------------------
# Summarization function
# ------------------------------
def summarize_text(text: str) -> str:
    """
    Summarizes a concert tour document using Gemini LLM.
    Returns bullet points with a confirmation message.
    """
    if not text.strip():
        return "The provided document is empty or invalid."

    prompt = f"""
    Summarize the following concert tour document in concise bullet points
    (dates, artists, venues, special guests, and logistics):

    {text}

    Summary:
    """
    try:
        response = gemini_llm.invoke(prompt)

        # Handle multiple response types
        if isinstance(response, AIMessage):
            summary = response.content.strip()
        elif isinstance(response, str):
            summary = response.strip()
        else:
            logger.warning(f"Unexpected response type: {type(response)}")
            return "Failed to generate a valid summary. Unexpected response type."

        return (
            "✅ Thank you! Your document has been successfully added to the database.\n"
            "Here is a brief summary of the document:\n\n"
            f"{summary}"
        )

    except Exception as e:
        logger.error(f"Error occurred while summarizing text: {e}")
        return f"Error occurred while summarizing the text: {e}"
