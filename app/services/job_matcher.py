from datetime import datetime
from app.db.session import initialize_db
from app.services.ai_engine import tag_match_description_with_ai

def _save_matching_result(db, match_data, user_id, job_id, path_segment):
    ref = db.reference(f"{user_id}/jobs/{path_segment}/{job_id}")
    existing_data = ref.get()

    # Check if this job has already been matched to avoid redundant AI calls/writes
    if existing_data["match_date"] != "false":
        return 

    match_date = datetime.now().isoformat()

    # If match_data is a DICT, use .get(). If it's an OBJECT, use getattr().
    # Assuming it's an object based on your previous code:
    payload = {
        'match_percentage': getattr(match_data, 'match_percentage', 0),
        'matching_points': getattr(match_data, 'matching_points', []),
        'missing_points': getattr(match_data, 'missing_points', []),
        'summary': getattr(match_data, 'summary', ""),
        'match_date': match_date
    }

    ref.update(payload)

def _process_job_matches(db, user_id, jobs_dict, context_tags, path_segment):
    if not jobs_dict:
        return

    for job_id, job_info in jobs_dict.items():
        match_data = tag_match_description_with_ai(
            context_tags['edu'], 
            context_tags['title'], 
            context_tags['skills'], 
            job_info.get("description", "")
        )
        _save_matching_result(db, match_data, user_id, job_id, path_segment)

def tag_match_description(user_id):
    db = initialize_db()
    
    # Extracts context tags
    context_tags = {
        'edu': db.reference(f"{user_id}/tags/education").get(),
        'title': db.reference(f"{user_id}/tags/job_title").get(),
        'skills': db.reference(f"{user_id}/tags/skills").get()
    }
    
    # Processes job categories
    categories = ['education', 'title']
    for category in categories:
        jobs_ref = db.reference(f"{user_id}/jobs/{category}").get()
        _process_job_matches(db, user_id, jobs_ref, context_tags, category)

    print(f"Successfully matched user {user_id} with jobs.")