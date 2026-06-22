"""
Insight model — represents a document in the `insights` collection.
Stores AI-agent-generated outputs so the dashboard can show history
without recomputing every time.
"""
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional, Literal, Any, Dict
from bson import ObjectId

InsightType = Literal[
    "expense_analysis", "savings_recommendation", "goal_prediction",
    "reminder_alert", "financial_health_score", "monthly_report", "chat_response",
]


class InsightModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    type: InsightType
    title: str
    content: str
    data: Optional[Dict[str, Any]] = {}
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


def insight_doc_to_dict(doc: dict) -> dict:
    if not doc:
        return None
    return {
        "id": str(doc["_id"]),
        "user_id": doc.get("user_id"),
        "type": doc.get("type"),
        "title": doc.get("title"),
        "content": doc.get("content"),
        "data": doc.get("data", {}),
        "created_at": doc.get("created_at"),
    }
