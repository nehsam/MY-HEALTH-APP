from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class UserSessionContext(BaseModel):
   
    name: str
    uid: int

    goal: Optional[dict] = None
    diet_preferences: Optional[str] = None
    workout_plan: Optional[dict] = None
    meal_plan: Optional[List[str]] = None
    injury_notes: Optional[str] = None

    handoff_logs: List[str] = Field(default_factory=list)
    progress_logs: List[Dict[str, str]] = Field(default_factory=list)
