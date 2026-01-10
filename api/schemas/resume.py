from pydantic import BaseModel
from typing import List

class CVProfile(BaseModel):
    qualifications: List[str]
    working_experience: List[str]
    education: List[str]
    top_skills: List[str]