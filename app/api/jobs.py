from fastapi import APIRouter, BackgroundTasks
from app.services.job_matcher import tag_match_description
from app.services.job_service import fetch_job_ads

router = APIRouter()

@router.post("/fetchjobs")
async def fetch_jobs(user_id: str, municipality: str):
    fetch_job_ads(user_id, municipality)
    return {"status": "success"}

@router.post("/matchjobs")
async def match_jobs(user_id: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(tag_match_description, user_id)
    return {"status": "processing"}