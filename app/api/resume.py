from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_engine import AIEngine
from app.db.firebase_admin import initialize_db
from app.kafka.producer import MessageProducer

db = initialize_db()
ai_engine = AIEngine(db)
producer = MessageProducer()

class ResumeData(BaseModel):
    user_id: str
    resume: str

router = APIRouter()

@router.post("/createusertags")
async def extract_user_tags(data: ResumeData):

    # Validation
    if not data.resume or not data.user_id:
        raise HTTPException(status_code=400, detail="Missing data")
    
    try:
        producer.send_resume_event(data.user_id, data.resume)
        # Extract and Save Tags
        response = ai_engine.extract_resume_tags(data.user_id, data.resume)
        if not response:
            raise HTTPException(status_code=503, detail="AI Service overloaded")

        return {
            "status": "success", 
            "message": f"Tags extracted and jobs fetched for {data.user_id}"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))