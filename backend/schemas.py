from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# Each model defines one MongoDB collection: class name lowercased

class Lead(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    title: Optional[str] = None
    linkedin_url: Optional[str] = None
    source: Optional[str] = Field(default="manual")
    tags: List[str] = Field(default_factory=list)
    notes: Optional[str] = None

class IntentSignal(BaseModel):
    company: str
    type: str  # e.g., hiring-surge, job-title-hiring, recent-joiner, site-visit, social-engagement, traffic-change, ads-budget-change, tech-stack
    detail: Optional[str] = None
    value: Optional[str] = None

class Campaign(BaseModel):
    name: str
    objective: str
    persona: Optional[str] = None
    status: str = Field(default="draft")

class MeetingRequest(BaseModel):
    company: str
    contact_email: EmailStr
    contact_name: Optional[str] = None
    business_model: str
    goals: Optional[str] = None

class PersonaWorkshopInput(BaseModel):
    crm_contact_ids: List[str]
    success_criteria: Optional[str] = None

class CopywritingInput(BaseModel):
    persona: str
    pains: List[str]
    vocabulary: List[str]

class ColdCallerMatchInput(BaseModel):
    industry: str
    target_roles: List[str]

class LaunchInput(BaseModel):
    campaign_id: str
