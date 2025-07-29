from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import run_research
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.post("/research")
async def research_route(data: QueryRequest):
    report = run_research(data.query)
    return {"result": report}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)