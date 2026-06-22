"""
Goal model — represents a document in the `goals` collection.
e.g. "Save ₹60,000 for a laptop by December".
"""
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional, Literal
from bson import ObjectId

GoalStatus = Literal["active", "completed", "abandoned"]


class GoalModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    title: str
    target_amount: float
    current_amount: float = 0.0
    target_date: Optional[datetime] = None
    status: GoalStatus = "active"
    notes: Optional[str] = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


def goal_doc_to_dict(doc: dict) -> dict:
    if not doc:
        return None
    return {
        "id": str(doc["_id"]),
        "user_id": doc.get("user_id"),
        "title": doc.get("title"),
        "target_amount": doc.get("target_amount"),
        "current_amount": doc.get("current_amount", 0.0),
        "target_date": doc.get("target_date"),
        "status": doc.get("status", "active"),
        "notes": doc.get("notes", ""),
        "progress_percent": round(
            (doc.get("current_amount", 0.0) / doc["target_amount"]) * 100, 2
        ) if doc.get("target_amount") else 0.0,
        "created_at": doc.get("created_at"),
    }
