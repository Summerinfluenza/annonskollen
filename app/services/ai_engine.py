import os
from google import genai
from pydantic import BaseModel
from typing import List, Union
from dotenv import load_dotenv

load_dotenv()

class ResumeTags(BaseModel):
    skills: List[str]
    education: List[str]
    experience: List[str]
    keywords_skills: List[str]
    keywords_education: List[str]
    keywords_experience: List[str]

class JobMatchResult(BaseModel):
    match_education: str
    match_percentage: int
    matching_points: List[str]
    missing_points: List[str]
    summary: str
    apply: str

class AIEngine:
    def __init__(self, db_instance):
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.tagger_model = "gemini-2.5-flash"
        self.matcher_model = "gemini-2.5-flash-lite"
        self.db = db_instance

    def _format_list(self, data: Union[List[str], str]) -> str:
        if isinstance(data, list):
            return ", ".join(data)
        return data or ""
    
    def _save_user_tags(self, user_id, response_data):
        ref = self.db.reference(user_id).child("tags")
        ref.set(response_data.model_dump())
        return 

    def extract_resume_tags(self, user_id, resume_text: str) -> ResumeTags:
        prompt = f"""
        You are an elite HR Data Scientist. Your task is to transform raw resume text into a structured JSON profile optimized for the JobTech/Arbetsförmedlingen search API.

        ### Extraction Rules:
        1. **Skills**: Hard skills and high-value soft skills.
        2. **Education**: Summarize degrees.
        3. **Experience**: Identify most recent or relevant roles.
        4. **Keywords Education**: Industry job titles associated with this education (Swedish).
        5. **Keywords Title**: Standard industry titles the user is qualified for NOW.

        Resume Text:
        {resume_text}
        """
        try:
            response_data = self.client.models.generate_content(
                model=self.tagger_model,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": ResumeTags,
                }
            )
            self._save_user_tags(user_id, response_data.parsed)

            return True
        
        except Exception as e:
            if "503" in str(e):
                print("Model overloaded. Retrying via backoff...")
                return False
            raise e

    def match_job_description(self, education, experience, skills, job_description: str) -> JobMatchResult:
        """Critically compares user profile against a specific job description."""
        
        prompt = f"""
        You are an expert technical recruiter. Be critical.
        ### CANDIDATE DATA
        - Education: {self._format_list(education)}
        - Skills: {self._format_list(skills)}
        - Experience: {self._format_list(experience)}

        ### JOB DESCRIPTION
        {job_description}

        ### SCORING RULES
        1. Critical Match (30%): Exact technical skills/tools.
        2. Experience/Level (70%): Seniority match (Junior vs Senior).

        ### JSON STRUCTURE
        Return ONLY this JSON structure:
        {{
            "match_education": "true or false",
            "match_percentage": (int),
            "matching_points": ["List specific skills"],
            "missing_points": ["List specific gaps"],
            "summary": "One sentence explanation",
            "apply": "true or false"
        }}
        """
        response = self.client.models.generate_content(
            model=self.matcher_model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": JobMatchResult,
            }
        )
        return response.parsed