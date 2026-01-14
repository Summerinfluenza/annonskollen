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
    experience: List[str]
    keywords_skills: List[str]
    keywords_education: List[str]
    keywords_experience: List[str]

class JobMatchResult(BaseModel):
    match_education: str
    match_percentage: int
    matching_points: List[str] # Ensure this matches the prompt field
    missing_points: List[str]
    summary: str
    apply: str

# Model configuration
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
ai_model = "gemini-2.5-flash-lite"
ai_model_flash = "gemini-2.5-flash"

# Generates tags using AI based on the provided resume string
def extract_tags_with_ai(resume_text: str):
    try:
        prompt = f"""
        You are an elite HR Data Scientist. Your task is to transform raw resume text into a structured JSON profile optimized for the JobTech/Arbetsförmedlingen search API.

        ### Extraction Rules:
        1. **Skills**: Focus on hard skills (e.g., "Python", "Bokföring", "Projektledning") and high-value soft skills.
        2. **Education**: Summarize degrees (e.g., "MSc in Computer Science").
        3. **Experience**: Identify the most recent or relevant experience held by the user.
        4. **Keywords Education (Search Optimized)**: 
           - Generate keywords of relevant industry job titles associated with this education. Don't put seniority in it.
           - Use Swedish if the resume is Swedish; otherwise, provide the most likely Swedish search equivalent (e.g., "Sjuksköterska" for "Nurse").
        5. **Keywords Title (Search Optimized)**: 
           - Generate standard industry job titles the user is qualified for NOW, given their previous working experience.
           - Generate standard industry job titles the user is qualified for NOW, given their skills.
           - Avoid overly specific internal titles; use broad market terms (e.g., use "Systemutvecklare" instead of "Level 4 Ninja Coder").

        ### Critical Context:
        Be critical. If the experience is brief, do not label the user as "Senior". Ensure keywords are optimized for a 'q' parameter in a REST API.
        
        Resume Text:
        {resume_text}
        """

        response = client.models.generate_content(
            model=ai_model_flash,
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

# Matches education, work experience, and skills with the job description
def tag_match_description_with_ai(education, experience, skills, job_description):
    formatted_education = ", ".join(education) if isinstance(education, list) else education
    formatted_skills = ", ".join(skills) if isinstance(skills, list) else skills
    formatted_experience = ", ".join(experience) if isinstance(experience, list) else experience

    prompt = f"""
    You are an expert technical recruiter analyzing a job match. 
    Be critical. Do not give a high score unless the candidate truly meets the requirements.

    ### CANDIDATE DATA
    - Education: {formatted_education}
    - Skills: {formatted_skills}
    - Experience: {formatted_experience}

    ### JOB DESCRIPTION
    {job_description}

    ### SCORING RULES
    1. **Critical Match (30% of score):** Does the candidate have the exact technical skills (e.g., Python, C++) or specific tools (e.g., TestStand) listed as required?
    2. **Experience/Level (70% of score):** Does the candidate's seniority level match the job's expectations (Junior vs Senior)?

    ### OUTPUT INSTRUCTIONS
    - If the job description is in Swedish, analyze it but return the reasons in English.
    - Be specific. Instead of saying "Candidate has skills," say "Candidate matches Python and SQL requirements."
    - Be honest about gaps. If they don't have the exact skills listed or similar skills, and the relevant education background requires it, list that as a major gap.

    ### JSON STRUCTURE
    Return ONLY this JSON structure:
    {{
        "match_education": "true or false, indicating whether the candidate's education background matches the job role (ignoring seniority, skills and experience)",
        "match_percentage": (int),
        "matching_points": ["List specific skills found in both"],
        "missing_points": ["List specific requirements the candidate lacks"],
        "summary": "One sentence explaining why the score was given",
        "apply": "true or false, indicating whether it is worth the candidate applying for the job"
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