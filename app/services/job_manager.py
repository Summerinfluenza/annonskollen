import requests
import json
from datetime import datetime
from dotenv import load_dotenv
from app.services.ai_engine import AIEngine



load_dotenv()

class JobManager:
    def __init__(self, db_instance):
        self.db = db_instance
        self.base_url = "https://jobsearch.api.jobtechdev.se/search"
        self.headers = {'accept': 'application/json'}
        self.ai_engine = AIEngine(self.db)

    # --- Private Helper Methods ---

    def _fetch_from_api(self, params):
        response = requests.get(self.base_url, headers=self.headers, params=params)
        response.raise_for_status()
        return json.loads(response.content.decode('utf8'))

    def _save_raw_job(self, user_id, job_hit, category):
        ref = self.db.reference(f"{user_id}/jobs/{category}/{job_hit['id']}")
        ref.set({
            'job_id': job_hit['id'],
            'headline': job_hit['headline'],
            'employer': job_hit['employer']['name'],
            'deadline': job_hit['application_deadline'],
            'link': job_hit['webpage_url'],
            'description': job_hit['description']['text'],
            "match_date": "false",
            "match_percentage": 0
        })

    def _update_job_match(self, user_id, job_id, category, match_data):
        ref = self.db.reference(f"{user_id}/jobs/{category}/{job_id}")
        
        existing = ref.get()
        if existing and existing.get("match_date") != "false":
            return

        payload = {
            'match_education': getattr(match_data, 'match_education', 0),
            'match_percentage': getattr(match_data, 'match_percentage', 0),
            'matching_points': getattr(match_data, 'matching_points', []),
            'missing_points': getattr(match_data, 'missing_points', []),
            'summary': getattr(match_data, 'summary', ""),
            'match_date': datetime.now().isoformat(),
            'apply': getattr(match_data, 'apply', ""),
        }
        ref.update(payload)

    # --- Public Methods ---

    def fetch_and_store_jobs(self, user_id, municipality):
        """Fetches jobs based on user tags and saves them to Firebase."""
        categories = ["keywords_education", "keywords_experience"]
        
        for cat in categories:
            tags = self.db.reference(f"{user_id}/tags/{cat}").get() or []
            db_category = "education" if "education" in cat else "experience"
            
            for tag in tags:
                params = {'q': f"{tag} {municipality}"}
                data = self._fetch_from_api(params)
                
                for hit in data.get('hits', []):
                    self._save_raw_job(user_id, hit, db_category)
        
        print(f"Jobs fetched and stored for user {user_id}.")

    def match_jobs_with_ai(self, user_id):
        context = {
            'education': self.db.reference(f"{user_id}/tags/education").get(),
            'experience': self.db.reference(f"{user_id}/tags/experience").get(),
            'skills': self.db.reference(f"{user_id}/tags/skills").get()
        }

        for category in ['education', 'experience']:
            jobs = self.db.reference(f"{user_id}/jobs/{category}").get() or {}
            
            for job_id, job_info in jobs.items():
                match_result = self.ai_engine.match_job_description(
                    context['education'], 
                    context['experience'], 
                    context['skills'], 
                    job_info.get("description", "")
                )
                self._update_job_match(user_id, job_id, category, match_result)

        print(f"Successfully matched jobs for user {user_id}.")