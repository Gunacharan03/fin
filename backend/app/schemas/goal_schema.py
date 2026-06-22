from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal


class GoalCreateSchema(BaseModel):
    title: str = Field(..., min_length=2, max_length=120)
    target_amount: float = Field(..., gt=0)
    current_amount: float = Field(default=0.0, ge=0)
    target_date: Optional[datetime] = None
    notes: Optional[str] = ""


class GoalUpdateSchema(BaseModel):
    title: Optional[str] = None
    target_amount: Optional[float] = Field(default=None, gt=0)
    current_amount: Optional[float] = Field(default=None, ge=0)
    target_date: Optional[datetime] = None
    status: Optional[Literal["active", "completed", "abandoned"]] = None
    notes: Optional[str] = None


class GoalContributionSchema(BaseModel):
    amount: float = Field(..., gt=0)


class GoalResponseSchema(BaseModel):
    id: str
    user_id: str
    title: str
    target_amount: float
    current_amount: float
    target_date: Optional[datetime]
    status: str
    notes: str
    progress_percent: float
    created_at: datetime
