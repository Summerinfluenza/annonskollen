import os
from dotenv import load_dotenv
from database import intialize_db

load_dotenv()

test_user_id=os.getenv("USER_ID")

def _get_tags():
    db = intialize_db()
    edu_ref = db.reference(f"{test_user_id}/tags/education")
    title_ref = db.reference(f"{test_user_id}/tags/job_title")
    skills_ref = db.reference(f"{test_user_id}/tags/skills")
    return





