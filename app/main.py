from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from pprint import PrettyPrinter

from app.agents.application import tailor_profile_for_job

from .agents.company import linkedin_company_lookup
from .tools.jobs import get_jobs_list, get_job_details
from .tools.tools import extract_resume_info

app = FastAPI()

pp = PrettyPrinter(indent=4)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str


@app.get("/company")
async def get_company_linkedin(name: str):
    result = linkedin_company_lookup(name)
    return result


@app.post("/jobs")
async def get_jobs(job_description: QueryRequest, company: str, location: str):
    job_data = get_jobs_list(job_description.query, location, company)
    return job_data


@app.get("/description")
async def get_job_description(job_id: str):
    job_details = get_job_details(job_id)
    return job_details


@app.post("/application")
async def tailor_application(resume: UploadFile = File(...)):
    resume_path = f"/tmp/{resume.filename}"
    with open(resume_path, "wb") as f:
        f.write(await resume.read())
    resume_text = extract_resume_info(resume_path)
    return resume_text


@app.post("/tailorApp")
async def tailor_application(
    location: str = Form(...),
    job_description: str = Form(...),
    resume: UploadFile = File(...),
):
    resume_path = f"/tmp/{resume.filename}"
    with open(resume_path, "wb") as f:
        f.write(await resume.read())
    resume_text = extract_resume_info(resume_path)
    job_data = get_jobs_list(job_description, location, "")
    job_ids = [int(job["job_id"] )for job in job_data]
    result_list = []
    for job_id in job_ids[:3]:  # Limiting to first 3 jobs for brevity
        job_detail = get_job_details(job_id)
        result = tailor_profile_for_job(job_detail, resume_text)
        result_list.append(result)
    return result_list


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
