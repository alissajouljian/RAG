from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages.ai import AIMessage
from dotenv import load_dotenv
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

def summarize_text(text: str) -> str:
    """
    Summarizes a concert tour document using Gemini and returns bullet points with confirmation message.
    """
    if not text or len(text.strip()) == 0:
        return "The provided document is empty or invalid."

    prompt = f"""
    Summarize the following concert tour document in a few concise bullet points (dates, artists, venues, special guests, and logistics):
    {text}
    Summary:
    """
    try:
        response = llm.invoke(prompt)
        print("Full raw response:", response)
        if isinstance(response, AIMessage):
            summary = response.content.strip()
            return f"""Thank you for sharing! Your document has been successfully added to the database. 
                        Here is a brief summary of the data from the document:

                        {summary}"""
        
        return "Failed to generate a valid summary. Unexpected response type."

    except Exception as e:
        print(f"Error occurred while summarizing the text: {e}")
        return f"Error occurred while summarizing the text: {e}"
