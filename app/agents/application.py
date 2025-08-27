from langchain.agents import Tool
from langchain.agents import create_react_agent, AgentExecutor
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain_core.prompts import PromptTemplate
from langchain import hub
from pprint import PrettyPrinter

from ..tools.tools import get_profile_url_tavily

load_dotenv()
pp = PrettyPrinter(indent=4)
