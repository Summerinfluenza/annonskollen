import requests
import json
import os
from dotenv import load_dotenv
from database import initialize_db

load_dotenv()
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


def fetch_job_ads(user_id, municipality):
    db = initialize_db()
    edu_ref = db.reference(f"{user_id}/tags/keywords_education")
    title_ref = db.reference(f"{user_id}/tags/keywords_title")
    education_list = edu_ref.get() or []
    title_list = title_ref.get() or []

    for tag in education_list:
        search_params = {'q': f"{tag} {municipality}", 'limit': 5}
        json_response = _get_ads(search_params)
        _save_fetched_data_to_firebase(db, user_id, json_response, "education")
    
    for tag in title_list:
        search_params = {'q': f"{tag} {municipality}", 'limit': 5}
        json_response = _get_ads(search_params)
        _save_fetched_data_to_firebase(db, user_id, json_response, "title")

    print("Jobs fetched from Arbetsförmedlingen.")
    return json_response