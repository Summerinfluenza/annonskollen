from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.services.job_matcher import tag_match_description
from app.services.job_service import fetch_job_ads
from pydantic import BaseModel

class JobData(BaseModel):
    user_id: str
    municipality: str


router = APIRouter()

@router.post("/fetchjobs")
async def fetch_jobs(data: JobData):
    try:
        fetch_job_ads(data.user_id, data.municipality)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/matchjobs")
async def match_jobs(data: JobData, background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(tag_match_description, data.user_id)
        return {"status": "processing"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    