"""
Reminder routes: create, list (with upcoming/overdue filters), update,
mark as paid, delete.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from datetime import datetime, timezone, timedelta
from typing import Optional

from app.database import get_db
from app.schemas.reminder_schema import ReminderCreateSchema, ReminderUpdateSchema
from app.auth.jwt_handler import get_current_user
from app.utils.validators import validate_object_id, ensure_owner
from app.models.reminder_model import reminder_doc_to_dict

router = APIRouter(prefix="/api/reminders", tags=["Reminders"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_reminder(
    payload: ReminderCreateSchema,
    current_user: dict = Depends(get_current_user),
):
    db = get_db()
    doc = payload.model_dump()
    doc["user_id"] = str(current_user["_id"])
    doc["status"] = "pending"
    doc["created_at"] = datetime.now(timezone.utc)

    result = await db.reminders.insert_one(doc)
    doc["_id"] = result.inserted_id
    return reminder_doc_to_dict(doc)


@router.get("")
async def list_reminders(
    upcoming_days: Optional[int] = Query(default=None, description="Only show reminders due within N days"),
    status_filter: Optional[str] = Query(default=None, alias="status"),
    current_user: dict = Depends(get_current_user),
):
    db = get_db()
    query = {"user_id": str(current_user["_id"])}

    now = datetime.now(timezone.utc)

    # Auto-flag overdue reminders before returning them
    await db.reminders.update_many(
        {"user_id": str(current_user["_id"]), "status": "pending", "due_date": {"$lt": now}},
        {"$set": {"status": "overdue"}},
    )

    if status_filter:
        query["status"] = status_filter
    if upcoming_days is not None:
        query["due_date"] = {"$gte": now, "$lte": now + timedelta(days=upcoming_days)}

    cursor = db.reminders.find(query).sort("due_date", 1)
    docs = [reminder_doc_to_dict(doc) async for doc in cursor]
    return {"items": docs, "total": len(docs)}


@router.get("/{reminder_id}")
async def get_reminder(reminder_id: str, current_user: dict = Depends(get_current_user)):
    db = get_db()
    oid = validate_object_id(reminder_id, "reminder")
    doc = await db.reminders.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Reminder not found")
    ensure_owner(doc["user_id"], str(current_user["_id"]))
    return reminder_doc_to_dict(doc)


@router.put("/{reminder_id}")
async def update_reminder(
    reminder_id: str,
    payload: ReminderUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    db = get_db()
    oid = validate_object_id(reminder_id, "reminder")
    doc = await db.reminders.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Reminder not found")
    ensure_owner(doc["user_id"], str(current_user["_id"]))

    updates = {k: v for k, v in payload.model_dump().items() if v is not None}
    if updates:
        await db.reminders.update_one({"_id": oid}, {"$set": updates})

    updated_doc = await db.reminders.find_one({"_id": oid})
    return reminder_doc_to_dict(updated_doc)


@router.post("/{reminder_id}/mark-paid")
async def mark_reminder_paid(reminder_id: str, current_user: dict = Depends(get_current_user)):
    """Marks paid; if recurring, automatically creates the next occurrence."""
    db = get_db()
    oid = validate_object_id(reminder_id, "reminder")
    doc = await db.reminders.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Reminder not found")
    ensure_owner(doc["user_id"], str(current_user["_id"]))

    await db.reminders.update_one({"_id": oid}, {"$set": {"status": "paid"}})

    frequency = doc.get("frequency", "once")
    if frequency != "once":
        delta_map = {
            "weekly": timedelta(weeks=1),
            "monthly": timedelta(days=30),
            "yearly": timedelta(days=365),
        }
        next_due = doc["due_date"] + delta_map.get(frequency, timedelta(days=30))
        new_doc = {
            "user_id": doc["user_id"],
            "title": doc["title"],
            "amount": doc["amount"],
            "due_date": next_due,
            "frequency": frequency,
            "status": "pending",
            "category": doc.get("category", "EMI"),
            "notes": doc.get("notes", ""),
            "created_at": datetime.now(timezone.utc),
        }
        await db.reminders.insert_one(new_doc)

    updated_doc = await db.reminders.find_one({"_id": oid})
    return reminder_doc_to_dict(updated_doc)


@router.delete("/{reminder_id}", status_code=status.HTTP_200_OK)
async def delete_reminder(reminder_id: str, current_user: dict = Depends(get_current_user)):
    db = get_db()
    oid = validate_object_id(reminder_id, "reminder")
    doc = await db.reminders.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Reminder not found")
    ensure_owner(doc["user_id"], str(current_user["_id"]))

    await db.reminders.delete_one({"_id": oid})
    return {"message": "Reminder deleted successfully"}
