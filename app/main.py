from parser import convert_pdf_to_string
from tagger import extract_tags
from matcher import tag_match_description
from fetchjobs import fetch_job_ads
from pathlib import Path
from fetchjobs import fetch_job_ads
import os
from dotenv import load_dotenv
from database import initialize_db

load_dotenv()

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
    
    

