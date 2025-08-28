from langchain.agents import Tool
from langchain.agents import create_react_agent, AgentExecutor
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain_core.prompts import PromptTemplate
from langchain import hub
from pprint import PrettyPrinter

from app.tools.jobs import get_job_details

from ..tools.tools import get_profile_url_tavily

load_dotenv()
pp = PrettyPrinter(indent=4)


def tailor_profile_for_job(job, resume_text):
    tailoring_template = """
    Given a job description {job} , I want you to:
    1. See if the the resume {resume_text} has the relevant skills and experience to apply for the job
    2. If so, compose a cover letter highlighting the skills present on the resume and how they are relevant to the job.
    """
    # TODO: 2. If so, tailor the resume to highlight those skills and experience
    """
        Given the following job description:
    {job}

    And the following resume:
    {resume_text}

    Please:
    1. Identify the relevant skills and experience in the resume that match the job description.
    2. Tailor the resume to highlight those skills and experiences for this job.
    3. Summarize the tailored resume in a structured format suitable for a PDF export (e.g., sections for Skills, Experience, Education).

    Output your response in markdown so it can be easily converted to a PDF.
    """
    tailoring_prompt_template = PromptTemplate(
    input_variables=["job","resume"], template=tailoring_template
    )
    llm = ChatOpenAI(
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        temperature=0,
        model_name="gpt-4o-mini",
    )
    chain = tailoring_prompt_template | llm
    res = chain.invoke(input={"job": job, "resume_text": resume_text})
    return res.content

    # BELOW CODE IS FOR AGENT-BASED APPROACH, BUT FOR NOW WE ARE USING A SIMPLE CHAIN
    # tools_for_agent = [
    #     Tool(
    #         name="Get Job Details",
    #         func=get_job_details,
    #         description="Useful for looking up a job description given a job ID.",
    #     )
    # ]
    # react_prompt = hub.pull("hwchase17/react")
    # agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    # agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)
    # result = agent_executor.invoke(
    #     input={"input": tailoring_prompt_template.format(job=job, resume_text=resume_text)}
    # )
    # return result["output"]