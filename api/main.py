from parser import convert_pdf_to_string
from tagger import extract_tags
from matcher import tag_match_description
from fetchjobs import fetch_job_ads
from pathlib import Path
from fetchjobs import fetch_job_ads
import os
from dotenv import load_dotenv
from database import intialize_db

load_dotenv()

# Finds the file
DATA_DIR = Path(__file__).parent / "data"
sample_pdf = DATA_DIR / "testresume.pdf"
test_user_id=os.getenv("USER_ID")
municipality=os.getenv("MUNICIPALITY")
db = intialize_db()

# Test it
if __name__ == "__main__":
    #Reads and extracts pdf into a string
    content_from_pdf = convert_pdf_to_string(sample_pdf)

    #Reads the string and extract relevant information into list of tags
    #extract_tags(content_from_pdf)

    ##___________________________________________________________________
    # Extracts jobs and saves to user_id based upon education or skills
    edu_ref = db.reference(f"{test_user_id}/tags/keywords_education")
    title_ref = db.reference(f"{test_user_id}/tags/keywords_title")
    education_list = edu_ref.get() or []
    title_list = title_ref.get() or []

    for tag in education_list:
        fetch_job_ads(f"{tag} {municipality}", "education")
    
    for tag in title_list:
        fetch_job_ads(f"{tag} {municipality}", "title")
    ##___________________________________________________________________


    #___________________________________________________________________
    #Matches user tags with jobs

    edu_ref = db.reference(f"{test_user_id}/tags/education").get()
    title_ref = db.reference(f"{test_user_id}/tags/job_title").get()
    skills_ref = db.reference(f"{test_user_id}/tags/skills").get()

    jobs_ref = db.reference(f"{test_user_id}/jobs/education").get()
    for job in jobs_ref.items():
        job_description = job[1]["description"]
        job_id = job[1]["job_id"]
        
        tag_match_description(test_user_id, job_id, edu_ref, title_ref, skills_ref, job_description)
        break
    #___________________________________________________________________
    
    

