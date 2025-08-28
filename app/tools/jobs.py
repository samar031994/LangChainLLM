import os
import requests
from pprint import PrettyPrinter
from dotenv import load_dotenv

load_dotenv()
pp = PrettyPrinter(indent=4)

def get_jobs_list(details: str, location: str, company: str):
    url = "https://api.scrapingdog.com/linkedinjobs"
    
    params = {
        "api_key": os.environ.get("SCRAPIN_DOG_API_KEY"),
        "field": details,
        "geoid": "",
        "location": location,
        "page": 1,
        "job_type": "full_time",
        "exp_level": "associate",
        "filter_by_company": company if company else "",
        }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data

def get_job_details(job_id: str):
    url = "https://api.scrapingdog.com/linkedinjobs"
    params = {
        "api_key": os.environ.get("SCRAPIN_DOG_API_KEY"),
        "job_id": job_id
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data
