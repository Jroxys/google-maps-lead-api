from pydantic import BaseModel
from typing import Optional, List

class LeadRequest(BaseModel):
    keyword: str
    location: str
    limit: int = 50

class Lead(BaseModel):
    name: str
    website: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    rating: Optional[str]

class JobStatus(BaseModel):
    job_id: str
    status: str
    total_leads: Optional[int] = 0
