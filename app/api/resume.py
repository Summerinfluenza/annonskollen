from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf_parser import convert_pdf_to_string
from app.services.user_tagger import extract_tags
from pathlib import Path
import shutil

router = APIRouter()
user_resume_cache = {}

@router.post("/createusertags")
async def extract_user_tags(user_id: str, file: UploadFile = File(...)):
    # Saves the uploaded file temporarily
    temp_path = Path(f"temp_{user_id}.pdf")
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Extracts text using parser
    resume_text = convert_pdf_to_string(temp_path)
    user_resume_cache[user_id] = resume_text
    
    # Cleans up
    temp_path.unlink() 

    # Processes resume and extracts usertags
    resume_text = user_resume_cache.get(user_id)
    if not resume_text:
        raise HTTPException(status_code=400, detail="No resume text found. Run /convertfile first.")
    
    extract_tags(resume_text, user_id)
    return {"status": "success", "message": f"Tags extracted for {user_id}"}