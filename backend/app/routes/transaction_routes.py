"""
Transaction routes: create, list (with filters), get one, update, delete.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from datetime import datetime
from typing import Optional, Literal

from app.database import get_db
from app.schemas.transaction_schema import TransactionCreateSchema, TransactionUpdateSchema
from app.auth.jwt_handler import get_current_user
from app.utils.validators import validate_object_id, ensure_owner
from app.models.transaction_model import transaction_doc_to_dict

router = APIRouter(prefix="/api/transactions", tags=["Transactions"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_transaction(
    payload: TransactionCreateSchema,
    current_user: dict = Depends(get_current_user),
):
    db = get_db()
    doc = payload.model_dump()
    doc["user_id"] = str(current_user["_id"])
    doc["source"] = "manual"
    doc["created_at"] = datetime.utcnow()

    result = await db.transactions.insert_one(doc)
    doc["_id"] = result.inserted_id
    return transaction_doc_to_dict(doc)


@router.get("")
async def list_transactions(
    type: Optional[Literal["income", "expense"]] = Query(default=None),
    category: Optional[str] = Query(default=None),
    start_date: Optional[datetime] = Query(default=None),
    end_date: Optional[datetime] = Query(default=None),
    limit: int = Query(default=100, le=500),
    skip: int = Query(default=0, ge=0),
    current_user: dict = Depends(get_current_user),
):
    db = get_db()
    query = {"user_id": str(current_user["_id"])}
    if type:
        query["type"] = type
    if category:
        query["category"] = category
    if start_date or end_date:
        query["date"] = {}
        if start_date:
            query["date"]["$gte"] = start_date
        if end_date:
            query["date"]["$lte"] = end_date

    cursor = db.transactions.find(query).sort("date", -1).skip(skip).limit(limit)
    docs = [transaction_doc_to_dict(doc) async for doc in cursor]
    total = await db.transactions.count_documents(query)
    return {"items": docs, "total": total}


@router.get("/{transaction_id}")
async def get_transaction(
    transaction_id: str,
    current_user: dict = Depends(get_current_user),
):
    db = get_db()
    oid = validate_object_id(transaction_id, "transaction")
    doc = await db.transactions.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Transaction not found")
    ensure_owner(doc["user_id"], str(current_user["_id"]))
    return transaction_doc_to_dict(doc)


@router.put("/{transaction_id}")
async def update_transaction(
    transaction_id: str,
    payload: TransactionUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    db = get_db()
    oid = validate_object_id(transaction_id, "transaction")
    doc = await db.transactions.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Transaction not found")
    ensure_owner(doc["user_id"], str(current_user["_id"]))

    updates = {k: v for k, v in payload.model_dump().items() if v is not None}
    if updates:
        await db.transactions.update_one({"_id": oid}, {"$set": updates})

    updated_doc = await db.transactions.find_one({"_id": oid})
    return transaction_doc_to_dict(updated_doc)


@router.delete("/{transaction_id}", status_code=status.HTTP_200_OK)
async def delete_transaction(
    transaction_id: str,
    current_user: dict = Depends(get_current_user),
):
    db = get_db()
    oid = validate_object_id(transaction_id, "transaction")
    doc = await db.transactions.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Transaction not found")
    ensure_owner(doc["user_id"], str(current_user["_id"]))

    await db.transactions.delete_one({"_id": oid})
    return {"message": "Transaction deleted successfully"}
