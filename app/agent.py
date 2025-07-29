from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()

llm = OpenAI(openai_api_key=os.environ.get('OPENAI_API_KEY'),temperature=0)

search = SerpAPIWrapper(serpapi_api_key=os.environ.get('SERPAPI_API_KEY'))
tools = [
    Tool(name="Web Search", func=search.run, description="Search the internet")
]

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

def run_research(query: str):
    result = agent.run(f"Do detailed research on: {query}. Summarize findings in 3 sections.")
    return result