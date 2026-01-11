from app.services.pdf_parser import convert_pdf_to_string
from app.services.user_tagger import extract_tags
from app.services.job_matcher import tag_match_description
from app.services.job_service import fetch_job_ads
from pathlib import Path
from app.services.job_service import fetch_job_ads
import os
from dotenv import load_dotenv
from app.db.session import initialize_db
from fastapi import FastAPI, BackgroundTasks
load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "FastAPI is running!"}

# Finds the file
DATA_DIR = Path(__file__).parent / "data"
sample_pdf = DATA_DIR / "testresume.pdf"
test_user_id=os.getenv("USER_ID")
municipality=os.getenv("MUNICIPALITY")
db = initialize_db()

# Test it
if __name__ == "__main__":

    ##___________________________________________________________________
    #Reads and extracts pdf into a string
    resume_text = convert_pdf_to_string(sample_pdf)
    ##___________________________________________________________________

    ##___________________________________________________________________
    #Reads the string and extract relevant information into list of tags
    extract_tags(resume_text, test_user_id)
    ##___________________________________________________________________

    ##___________________________________________________________________
    # Extracts jobs and saves to user_id based upon education or skills
    fetch_job_ads(test_user_id, municipality)
    ##___________________________________________________________________

    #___________________________________________________________________
    #Matches user tags with jobs
    tag_match_description(test_user_id)
    #___________________________________________________________________
    
    

