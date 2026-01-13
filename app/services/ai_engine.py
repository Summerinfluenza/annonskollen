from google import genai
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()

# Tag structure for resume
class ResumeTags(BaseModel):
    skills: List[str]
    education: List[str]
    job_title: List[str]
    keywords_education: List[str]
    keywords_title: List[str]

class JobMatchResult(BaseModel):
    match_percentage: int
    matching_points: List[str]
    missing_points: List[str]
    summary: str

#Model configuration
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
ai_model = "gemini-2.5-flash-lite"

#Creates tags with gemini based on the provided resume string
def extract_tags_with_ai(resume_text: str):
    try:
        prompt = f"""
        You are an elite HR Data Scientist. Your task is to transform raw resume text into a structured JSON profile optimized for the JobTech/Arbetsförmedlingen search API.

        ### Extraction Rules:
        1. **Skills**: Focus on hard skills (e.g., "Python", "Bokföring", "Projektledning") and high-value soft skills.
        2. **Education**: Summarize degrees and institutions (e.g., "MSc in Computer Science, KTH").
        3. **Job Titles**: Identify the most recent or relevant job titles held by the user.
        4. **Keywords Education (Search Optimized)**: 
           - Generate 3-5 keywords that a recruiter would use to find this education.
           - Use Swedish if the resume is Swedish; otherwise, provide the most likely Swedish search equivalent (e.g., "Sjuksköterska" for "Nurse").
        5. **Keywords Title (Search Optimized)**: 
           - Generate 3-5 standard industry job titles the user is qualified for NOW.
           - Avoid overly specific internal titles; use broad market terms (e.g., use "Systemutvecklare" instead of "Level 4 Ninja Coder").

        ### Critical Context:
        Be critical. If the experience is brief, do not label them as "Senior". Ensure keywords are optimized for a 'q' parameter in a REST API.
        
        Resume Text:
        {resume_text}
        """

        response = client.models.generate_content(
            model=ai_model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": ResumeTags,
            }
        )
        structured_data = response.parsed
        return structured_data
    except Exception as e:
        if "503" in str(e):
            print("Model overloaded. Retrying via backoff...")
            return {"error": "Service temporarily busy. Please try again in a moment."}
        raise e

def tag_match_description_with_ai(education, job_title, skills, job_description):
    formatted_education = ", ".join(education) if isinstance(education, list) else education
    formatted_skills = ", ".join(skills) if isinstance(skills, list) else skills
    formatted_job_title = ", ".join(job_title) if isinstance(job_title, list) else job_title

    prompt = f"""
    You are an expert technical recruiter analyzing a job match. 
    Be critical. Do not give a high score unless the candidate truly meets the requirements.

    ### CANDIDATE DATA
    - Education: {formatted_education}
    - Skills: {formatted_skills}
    - Job experience: {formatted_job_title}

    ### JOB DESCRIPTION
    {job_description}

    ### SCORING RULES
    1. **Critical Match (20% of score):** Does the candidate have the exact technical skills (e.g., Python, C++) or specific tools (e.g., TestStand) listed as required?
    2. **Education Match (40% of score):** Does the degree level and field (e.g., bachelor Programming) align with the job's industry?
    3. **Experience/Level (40% of score):** Does the candidate's seniority level match the job's expectations (Junior vs Senior)?

    ### OUTPUT INSTRUCTIONS
    - If the job description is in Swedish, analyze it but return the reasons in English.
    - Be specific. Instead of "Candidate has skills," say "Candidate matches Python and SQL requirements."
    - Be honest about gaps. If they don't have the exact skills listed or similiar skills and the job requires it, list that as a major gap.

    ### JSON STRUCTURE
    Return ONLY this JSON structure:
    {{
        "match_percentage": (int),
        "match_points": ["List specific skills found in both"],
        "missing_points": ["List specific requirements the candidate lacks"],
        "summary": "One sentence explaining why the score was given"
    }}
    """

    response = client.models.generate_content(
        model=ai_model,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": JobMatchResult,
        }
    )
    structured_data = response.parsed
    return structured_data

