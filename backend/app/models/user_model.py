"""
User model — represents a document in the `users` MongoDB collection.

We use plain Pydantic models (not an ODM) since Motor talks to MongoDB
directly via dicts. Models here define the *shape* of documents for
type safety and serialization, not active-record behavior.
"""
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime, timezone
from typing import Optional
from bson import ObjectId


class UserModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    email: EmailStr
    hashed_password: str
    monthly_income: float = 0.0
    currency: str = "INR"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


def user_doc_to_dict(doc: dict) -> dict:
    """Convert a raw MongoDB user document into a JSON-safe dict (no password)."""
    if not doc:
        return None
    return {
        "id": str(doc["_id"]),
        "name": doc.get("name"),
        "email": doc.get("email"),
        "monthly_income": doc.get("monthly_income", 0.0),
        "currency": doc.get("currency", "INR"),
        "created_at": doc.get("created_at"),
    }
