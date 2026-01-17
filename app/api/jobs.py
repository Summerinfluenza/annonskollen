from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.kafka.producer import MessageProducer

producer = MessageProducer()

class JobData(BaseModel):
    user_id: str
    municipality: str

router = APIRouter()

@router.post("/fetchjobs")
async def fetch_jobs(data: JobData):

    if not data.municipality or not data.user_id:
        raise HTTPException(status_code=400, detail="Missing data")

    try:
        producer.send_fetch_job_event(data.user_id, data.municipality)
        return {"status": "accepted"}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to queue task")
    

@router.post("/matchjobs")
async def match_jobs(data: JobData):
    if not data.user_id:
        raise HTTPException(status_code=400, detail="Missing data")

    try:
        producer.send_match_job_event(data.user_id)
        return {"status": "accepted"}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to queue task")
    