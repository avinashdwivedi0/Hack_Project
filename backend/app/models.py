from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr

class SkillTrack(BaseModel):
    id: Optional[str] = None
    skill_name: str
    week_number: int
    topics: List[str]
    video_links: List[str]

class QuizQ(BaseModel):
    id: Optional[str] = None
    skill_id: str
    question: str
    options: List[str]
    correct_answer: int

class QuizSubmit(BaseModel):
    user_id: str
    skill_id: str
    answers: List[int]  # index per question

class ProgressUpdate(BaseModel):
    user_id: str
    skill_id: str
    completed_percentage: float
    streak_days: int

class ChatIn(BaseModel):
    user_id: str
    message: str
    context: Optional[Dict[str, Any]] = None

class ChatOut(BaseModel):
    response: str
