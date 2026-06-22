"""
Goal routes: create, list, get one, update, contribute funds, delete.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timezone

from app.database import get_db
from app.schemas.goal_schema import GoalCreateSchema, GoalUpdateSchema, GoalContributionSchema
from app.auth.jwt_handler import get_current_user
from app.utils.validators import validate_object_id, ensure_owner
from app.models.goal_model import goal_doc_to_dict

router = APIRouter(prefix="/api/goals", tags=["Goals"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_goal(
    payload: GoalCreateSchema,
    current_user: dict = Depends(get_current_user),
):
    db = get_db()
    now = datetime.now(timezone.utc)
    doc = payload.model_dump()
    doc["user_id"] = str(current_user["_id"])
    doc["status"] = "active"
    doc["created_at"] = now
    doc["updated_at"] = now

    result = await db.goals.insert_one(doc)
    doc["_id"] = result.inserted_id
    return goal_doc_to_dict(doc)


@router.get("")
async def list_goals(current_user: dict = Depends(get_current_user)):
    db = get_db()
    cursor = db.goals.find({"user_id": str(current_user["_id"])}).sort("created_at", -1)
    docs = [goal_doc_to_dict(doc) async for doc in cursor]
    return {"items": docs, "total": len(docs)}


@router.get("/{goal_id}")
async def get_goal(goal_id: str, current_user: dict = Depends(get_current_user)):
    db = get_db()
    oid = validate_object_id(goal_id, "goal")
    doc = await db.goals.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Goal not found")
    ensure_owner(doc["user_id"], str(current_user["_id"]))
    return goal_doc_to_dict(doc)


@router.put("/{goal_id}")
async def update_goal(
    goal_id: str,
    payload: GoalUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    db = get_db()
    oid = validate_object_id(goal_id, "goal")
    doc = await db.goals.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Goal not found")
    ensure_owner(doc["user_id"], str(current_user["_id"]))

    updates = {k: v for k, v in payload.model_dump().items() if v is not None}
    if updates:
        updates["updated_at"] = datetime.now(timezone.utc)
        await db.goals.update_one({"_id": oid}, {"$set": updates})

    updated_doc = await db.goals.find_one({"_id": oid})
    return goal_doc_to_dict(updated_doc)


@router.post("/{goal_id}/contribute")
async def contribute_to_goal(
    goal_id: str,
    payload: GoalContributionSchema,
    current_user: dict = Depends(get_current_user),
):
    """Add funds toward a goal; auto-marks as completed if target reached."""
    db = get_db()
    oid = validate_object_id(goal_id, "goal")
    doc = await db.goals.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Goal not found")
    ensure_owner(doc["user_id"], str(current_user["_id"]))

    new_amount = doc.get("current_amount", 0.0) + payload.amount
    new_status = "completed" if new_amount >= doc["target_amount"] else doc.get("status", "active")

    await db.goals.update_one(
        {"_id": oid},
        {"$set": {
            "current_amount": new_amount,
            "status": new_status,
            "updated_at": datetime.now(timezone.utc),
        }},
    )
    updated_doc = await db.goals.find_one({"_id": oid})
    return goal_doc_to_dict(updated_doc)


@router.delete("/{goal_id}", status_code=status.HTTP_200_OK)
async def delete_goal(goal_id: str, current_user: dict = Depends(get_current_user)):
    db = get_db()
    oid = validate_object_id(goal_id, "goal")
    doc = await db.goals.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Goal not found")
    ensure_owner(doc["user_id"], str(current_user["_id"]))

    await db.goals.delete_one({"_id": oid})
    return {"message": "Goal deleted successfully"}
