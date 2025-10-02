#online_lookup.py
import os
import json
import logging
from langchain_community.utilities import SerpAPIWrapper
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI

# ------------------------------
# Logging
# ------------------------------
logger = logging.getLogger(__name__)

# ------------------------------
# Search and LLM setup
# ------------------------------
search_wrapper = SerpAPIWrapper()

prompt_template = PromptTemplate(
    input_variables=["query"],
    template="""
    You are a concert tour assistant.
    Extract these details strictly in JSON format:
    1. Artist
    2. Tour Date
    3. Venue
    4. Short Summary

    Search Result:
    {query}
    """
)

llm_gemini = GoogleGenerativeAI(
    model='gemini-2.5-pro',
    api_key=os.getenv('GEMINI_API_KEY'),
    temperature=0.3
)

llm_chain = prompt_template | llm_gemini

# ------------------------------
# Online search function
# ------------------------------
def online_search(query: str) -> dict:
    """
    Perform an online search and return a structured JSON result.
    """
    try:
        # Get SERP results
        serp_result = search_wrapper.run(query)

        # Generate structured output with LLM
        result_text = llm_chain.invoke({"query": serp_result})
        try:
            return json.loads(result_text)
        except json.JSONDecodeError:
            return {"summary": result_text}

    except Exception as e:
        logger.error(f"Error in online_search: {e}")
        return {"error": str(e)}
