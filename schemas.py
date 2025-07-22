from pydantic import BaseModel
from datetime import date
from typing import List

class TaskCreate(BaseModel):
    title: str
    date: date
    completed: bool = False  # ✅ Add this line

class TaskOut(TaskCreate):
    id: int

    class Config:
        orm_mode = True

class ProfileBase(BaseModel):
    name: str
    email: str
    study_hours: int

class ProfileOut(ProfileBase):
    id: int
    class Config:
        orm_mode = True

class RecommendationRequest(BaseModel):
    new_title: str

class RecommendationResponse(BaseModel):
    recommendations: List[str]