"""
Transaction model — represents a document in the `transactions` collection.
Covers both income and expense entries.
"""
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional, Literal
from bson import ObjectId

TransactionType = Literal["income", "expense"]

EXPENSE_CATEGORIES = [
    "Food", "Groceries", "Rent", "Utilities", "Transport", "Fuel",
    "Shopping", "Entertainment", "Healthcare", "Education", "EMI",
    "Insurance", "Subscriptions", "Travel", "Investment", "Other",
]

INCOME_CATEGORIES = [
    "Salary", "Freelance", "Business", "Investment Returns", "Gift", "Other",
]


class TransactionModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    type: TransactionType
    amount: float
    category: str
    description: Optional[str] = ""
    date: datetime
    is_recurring: bool = False
    source: Literal["manual", "csv_upload"] = "manual"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


def transaction_doc_to_dict(doc: dict) -> dict:
    if not doc:
        return None
    return {
        "id": str(doc["_id"]),
        "user_id": doc.get("user_id"),
        "type": doc.get("type"),
        "amount": doc.get("amount"),
        "category": doc.get("category"),
        "description": doc.get("description", ""),
        "date": doc.get("date"),
        "is_recurring": doc.get("is_recurring", False),
        "source": doc.get("source", "manual"),
        "created_at": doc.get("created_at"),
    }
