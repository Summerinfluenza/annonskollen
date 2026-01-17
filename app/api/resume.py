from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.kafka.producer import MessageProducer

producer = MessageProducer()

class ResumeData(BaseModel):
    user_id: str
    resume: str

router = APIRouter()

@router.post("/createusertags")
async def extract_user_tags(data: ResumeData):
    if not data.resume or not data.user_id:
        raise HTTPException(status_code=400, detail="Missing data")

    try:
        producer.send_resume_event(data.user_id, data.resume)
        return {"status": "accepted"}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to queue task")