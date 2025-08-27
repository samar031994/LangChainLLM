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

def linkedin_company_lookup(name: str) -> str:
    llm = ChatOpenAI(
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        temperature=0,
        model_name="gpt-4o-mini",
    )
    template = """Given the company name {name_of_company}, I want you to get me a link to their linkedin profile.
    Your answer should contain only the link."""
    prompt_template = PromptTemplate(
        input_variables=["name_of_company"], template=template
    )
    tools_for_agent = [
        Tool(
            name="Crawl Google for linkedin profile page",
            func=get_profile_url_tavily,
            description="Useful for looking up a person's linkedin profile page.",
        )
    ]
    react_prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)
    result = agent_executor.invoke(
        input={"input": prompt_template.format(name_of_company=name)}
    )
    linkedin_url = result["output"]
    return linkedin_url


