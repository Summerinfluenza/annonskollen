import requests
import json
import os
from dotenv import load_dotenv
from database import intialize_db

load_dotenv()
url = 'https://jobsearch.api.jobtechdev.se'
url_for_search = f"{url}/search"

test_user_id=os.getenv("USER_ID")

def _get_ads(params):
    headers = {'accept': 'application/json'}
    response = requests.get(url_for_search, headers=headers, params=params)
    response.raise_for_status()  # check for http errors
    return json.loads(response.content.decode('utf8'))

def _save_fetched_data_to_firebase(json_response, keyword_type, user_id=test_user_id):
    hits = json_response['hits']
    db = intialize_db()
    ref = db.reference(f"{user_id}/jobs/{keyword_type}")

    for hit in hits:
        ref.child(hit['id']).set({
                'headline': hit['headline'],
                'employer': hit['employer']['name'],
                'deadline': hit['application_deadline'],
                'link': hit['webpage_url'],
                'description': hit['description']['text']
            })

    return

def fetch_job_ads(query, keyword_type):
    search_params = {'q': query, 'limit': 5}
    json_response = _get_ads(search_params)
    _save_fetched_data_to_firebase(json_response, keyword_type)
    return json_response