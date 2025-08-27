from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.document_loaders import PDFPlumberLoader


def get_profile_url_tavily(name: str):
    search = TavilySearchResults()
    result = search.run(f"{name}")
    return result

def extract_resume_info(resume_path: str):
    loader = PDFPlumberLoader(resume_path)
    docs = loader.load()
    return docs