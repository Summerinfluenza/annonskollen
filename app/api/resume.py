from fastapi import APIRouter, HTTPException
from app.services.user_tagger import extract_tags
from pydantic import BaseModel

class ResumeData(BaseModel):
    user_id: str
    resume: str

router = APIRouter()

@router.post("/createusertags")
async def extract_user_tags(data: ResumeData):

    if not data.resume:
        raise HTTPException(status_code=400, detail="No resume text found.")
    
    if not data.user_id:
        raise HTTPException(status_code=400, detail="No user id found.")
    
    extract_tags(data.resume, data.user_id)
    return {"status": "success", "message": f"Tags extracted for {data.user_id}"}