
from database import intialize_db
from ai_model import tag_match_description_with_ai
import re
import ast
from datetime import datetime

#Saves match results to db
def _save_matching_result(match_data, user_id, job_id):
    db = intialize_db()
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%dT%H:%M:%S")

    # Convert to string ONCE at the start to avoid the TypeError
    match_str = str(match_data)

    # 1. Extract Percentage
    match_percentage = re.search(r"match_percentage=(\d+)", match_str)
    percentage_val = int(match_percentage.group(1)) if match_percentage else 0

    # 2. Extract matching_points
    matching_match = re.search(r"matching_points=(\[.*?\])", match_str, re.DOTALL)
    matching_points = ast.literal_eval(matching_match.group(1)) if matching_match else []

    # 3. Extract missing_points
    missing_match = re.search(r"missing_points=(\[.*?\])", match_str, re.DOTALL)
    missing_points = ast.literal_eval(missing_match.group(1)) if missing_match else []

    # 4. Extract summary
    # Updated regex to be more flexible with the closing quote
    summary_match = re.search(r"summary=['\"](.*?)['\"]?$", match_str.strip(), re.DOTALL)
    summary = summary_match.group(1) if summary_match else ""

    ref = db.reference(f"{user_id}/jobs/education/{job_id}")
    ref.update({
        'match_percentage': percentage_val,
        'matching_points': matching_points,
        'missing_points': missing_points,
        'summary': summary,
        'match_date': formatted_date
    })
    return

def tag_match_description(user_id, job_id, education, job_title, skills, job_description):
    match_data = tag_match_description_with_ai(education, job_title, skills, job_description)
    print(job_id)
    _save_matching_result(match_data, user_id, job_id)
    return

