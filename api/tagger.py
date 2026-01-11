from database import intialize_db
from ai_model import extract_tags_with_ai

#Saves user tags to db
def _save_user_tags(tags_dict, user_id):
    db = intialize_db()
    ref = db.reference(user_id).child("tags")
    ref.set(tags_dict.model_dump())
    return 

#Creates user tags with gemini based on the provided resume string
def extract_tags(resume_text: str, user_id):
    structured_data = extract_tags_with_ai(resume_text)
    _save_user_tags(structured_data, user_id)
    return
