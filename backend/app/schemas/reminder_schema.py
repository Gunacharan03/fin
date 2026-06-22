from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal


class ReminderCreateSchema(BaseModel):
    title: str = Field(..., min_length=2, max_length=120)
    amount: float = Field(..., gt=0)
    due_date: datetime
    frequency: Literal["once", "monthly", "weekly", "yearly"] = "once"
    category: str = "EMI"
    notes: Optional[str] = ""


class ReminderUpdateSchema(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = Field(default=None, gt=0)
    due_date: Optional[datetime] = None
    frequency: Optional[Literal["once", "monthly", "weekly", "yearly"]] = None
    status: Optional[Literal["pending", "paid", "overdue"]] = None
    category: Optional[str] = None
    notes: Optional[str] = None


class ReminderResponseSchema(BaseModel):
    id: str
    user_id: str
    title: str
    amount: float
    due_date: datetime
    frequency: str
    status: str
    category: str
    notes: str
    created_at: datetime
