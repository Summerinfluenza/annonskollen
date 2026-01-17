from dotenv import load_dotenv
from fastapi import FastAPI
from app.api import resume, jobs

load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "FastAPI is running!"}

app.include_router(resume.router, prefix="/api", tags=["Resume Operations"])
app.include_router(jobs.router, prefix="/api", tags=["Job Matching"])
