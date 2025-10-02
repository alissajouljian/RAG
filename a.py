# from dotenv import load_dotenv
# import os
# import google.generativeai as genai
#
# # Load .env file
# load_dotenv()
#
# # Get Gemini API key
# api_key = os.getenv("GEMINI_API_KEY")
#
# # Configure Gemini client
# genai.configure(api_key=api_key)
#
# # List available models
# for model in genai.list_models():
#     print(model.name, model.supported_generation_methods)
from dotenv import load_dotenv
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Initialize ChatOpenAI with small model
llm_gpt = ChatOpenAI(
    model_name="gpt-3.5-turbo-16k",  # smaller, cheaper, less likely to hit quota
    temperature=0.3,
    openai_api_key=api_key
)

# Create a human message
human_message = HumanMessage(content="how are you")

# Generate response using .invoke()
response = llm_gpt.invoke([human_message])

# Print the text
print("\nGenerated Text:")
print(response.content)  # .invoke() returns a single message
