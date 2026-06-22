"""
Auth routes: register, login, get current profile, change password.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timezone

from app.database import get_db
from app.schemas.user_schema import (
    UserRegisterSchema, UserLoginSchema, TokenResponseSchema,
    UserResponseSchema, UserUpdateSchema, PasswordChangeSchema,
)
from app.auth.password_utils import hash_password, verify_password
from app.auth.jwt_handler import create_access_token, get_current_user
from app.models.user_model import user_doc_to_dict

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponseSchema, status_code=status.HTTP_201_CREATED)
async def register(payload: UserRegisterSchema):
    db = get_db()

    existing = await db.users.find_one({"email": payload.email})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        )

    now = datetime.now(timezone.utc)
    user_doc = {
        "name": payload.name,
        "email": payload.email,
        "hashed_password": hash_password(payload.password),
        "monthly_income": payload.monthly_income,
        "currency": payload.currency,
        "created_at": now,
        "updated_at": now,
    }
    result = await db.users.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id

    token = create_access_token(str(result.inserted_id), payload.email)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user_doc_to_dict(user_doc),
    }


@router.post("/login", response_model=TokenResponseSchema)
async def login(payload: UserLoginSchema):
    db = get_db()
    user_doc = await db.users.find_one({"email": payload.email})

    if not user_doc or not verify_password(payload.password, user_doc["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    token = create_access_token(str(user_doc["_id"]), user_doc["email"])
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user_doc_to_dict(user_doc),
    }


@router.get("/me", response_model=UserResponseSchema)
async def get_profile(current_user: dict = Depends(get_current_user)):
    return user_doc_to_dict(current_user)


@router.put("/me", response_model=UserResponseSchema)
async def update_profile(
    payload: UserUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    db = get_db()
    updates = {k: v for k, v in payload.model_dump().items() if v is not None}
    if updates:
        updates["updated_at"] = datetime.now(timezone.utc)
        await db.users.update_one({"_id": current_user["_id"]}, {"$set": updates})

    updated_doc = await db.users.find_one({"_id": current_user["_id"]})
    return user_doc_to_dict(updated_doc)


@router.post("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    payload: PasswordChangeSchema,
    current_user: dict = Depends(get_current_user),
):
    if not verify_password(payload.current_password, current_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )

    db = get_db()
    await db.users.update_one(
        {"_id": current_user["_id"]},
        {"$set": {
            "hashed_password": hash_password(payload.new_password),
            "updated_at": datetime.now(timezone.utc),
        }},
    )
    return {"message": "Password updated successfully"}
