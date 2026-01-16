from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from app.db.firebase_admin import initialize_db
from app.services.ai_engine import AIEngine
from app.services.job_manager import JobManager

db = initialize_db()
ai_engine = AIEngine(db)
job_manager = JobManager(db)

class JobData(BaseModel):
    user_id: str
    municipality: str

router = APIRouter()

@router.post("/fetchjobs")
async def fetch_jobs(data: JobData):
    try:
        job_manager.fetch_and_store_jobs(data.user_id, data.municipality)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/matchjobs")
async def match_jobs(data: JobData, background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(job_manager.match_jobs_with_ai, data.user_id)
        return {"status": "processing"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    