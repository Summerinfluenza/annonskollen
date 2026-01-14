import requests
import json
from dotenv import load_dotenv
from app.db.firebase_admin import initialize_db

load_dotenv()
# Government API for job fetch
url = 'https://jobsearch.api.jobtechdev.se'
url_for_search = f"{url}/search"


def _get_ads(params):
    headers = {'accept': 'application/json'}
    response = requests.get(url_for_search, headers=headers, params=params)
    response.raise_for_status()
    return json.loads(response.content.decode('utf8'))

def _save_fetched_data_to_firebase(db, user_id, json_response, keyword_type):
    hits = json_response['hits']
    ref = db.reference(f"{user_id}/jobs/{keyword_type}")

    for hit in hits:
        ref.child(hit['id']).set({
                'job_id': hit['id'],
                'headline': hit['headline'],
                'employer': hit['employer']['name'],
                'deadline': hit['application_deadline'],
                'link': hit['webpage_url'],
                'description': hit['description']['text'],
                "match_date": "false",
                "match_percentage": 0
            })
    return

# Fetches job and saves relevant information to the database 
def fetch_job_ads(user_id, municipality, limit=100):
    db = initialize_db()
    edu_ref = db.reference(f"{user_id}/tags/keywords_education")
    experience_ref = db.reference(f"{user_id}/tags/keywords_experience")
    education_list = edu_ref.get() or []
    experience_list = experience_ref.get() or []

    for tag in education_list:
        search_params = {'q': f"{tag} {municipality}", 'limit': limit}
        json_response = _get_ads(search_params)
        _save_fetched_data_to_firebase(db, user_id, json_response, "education")
    
    for tag in experience_list:
        search_params = {'q': f"{tag} {municipality}", 'limit': limit}
        json_response = _get_ads(search_params)
        _save_fetched_data_to_firebase(db, user_id, json_response, "experience")

    print("Jobs fetched from Arbetsförmedlingen.")
    return json_response