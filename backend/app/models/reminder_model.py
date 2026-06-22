"""
Reminder model — represents a document in the `reminders` collection.
Used for EMIs, bills, and other recurring or one-time payment reminders.
"""
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional, Literal
from bson import ObjectId

ReminderStatus = Literal["pending", "paid", "overdue"]
ReminderFrequency = Literal["once", "monthly", "weekly", "yearly"]


class ReminderModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    title: str
    amount: float
    due_date: datetime
    frequency: ReminderFrequency = "once"
    status: ReminderStatus = "pending"
    category: str = "EMI"
    notes: Optional[str] = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


def reminder_doc_to_dict(doc: dict) -> dict:
    if not doc:
        return None
    return {
        "id": str(doc["_id"]),
        "user_id": doc.get("user_id"),
        "title": doc.get("title"),
        "amount": doc.get("amount"),
        "due_date": doc.get("due_date"),
        "frequency": doc.get("frequency", "once"),
        "status": doc.get("status", "pending"),
        "category": doc.get("category", "EMI"),
        "notes": doc.get("notes", ""),
        "created_at": doc.get("created_at"),
    }
