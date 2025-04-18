import os
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.utilities import SerpAPIWrapper
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

search = SerpAPIWrapper()

prompt_template = PromptTemplate(
    input_variables=["query"],
    template="""
            You are a concert tour assistant. Use the following online search result to answer the query:
            Search Result:
            {query}
            Answer in a helpful, clear sentence summarizing key details.
            """
            )

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", api_key=os.getenv("GEMINI_API_KEY"))
llm_chain = LLMChain(llm=llm, prompt=prompt_template)

def online_search(query: str):
    serp_result = search.run(query)
    return llm_chain.run({"query": serp_result})
