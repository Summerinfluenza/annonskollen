from datetime import datetime
from app.db.firebase_admin import initialize_db
from app.services.ai_engine import tag_match_description_with_ai

def _save_matching_result(db, match_data, user_id, job_id, path_segment):
    ref = db.reference(f"{user_id}/jobs/{path_segment}/{job_id}")
    existing_data = ref.get()

    # Check if this job has already been matched to avoid redundant AI calls/writes
    if existing_data["match_date"] != "false":
        return 

    match_date = datetime.now().isoformat()

    payload = {
        'match_education': getattr(match_data, 'match_education', 0),
        'match_percentage': getattr(match_data, 'match_percentage', 0),
        'matching_points': getattr(match_data, 'matching_points', []),
        'missing_points': getattr(match_data, 'missing_points', []),
        'summary': getattr(match_data, 'summary', ""),
        'match_date': match_date,
        'apply': getattr(match_data, 'apply', ""),
    }

    ref.update(payload)


def _process_job_matches(db, user_id, jobs_dict, context_tags, path_segment):
    if not jobs_dict:
        return

    for job_id, job_info in jobs_dict.items():
        match_data = tag_match_description_with_ai(
            context_tags['education'], 
            context_tags['experience'], 
            context_tags['skills'], 
            job_info.get("description", "")
        )
        _save_matching_result(db, match_data, user_id, job_id, path_segment)

def tag_match_description(user_id):
    db = initialize_db()
    
    # Extracts context tags
    context_tags = {
        'education': db.reference(f"{user_id}/tags/education").get(),
        'experience': db.reference(f"{user_id}/tags/experience").get(),
        'skills': db.reference(f"{user_id}/tags/skills").get()
    }
    
    # Processes job categories
    categories = ['education', 'experience']
    for category in categories:
        jobs_ref = db.reference(f"{user_id}/jobs/{category}").get()
        _process_job_matches(db, user_id, jobs_ref, context_tags, category)

    print(f"Successfully matched user {user_id} with jobs.")