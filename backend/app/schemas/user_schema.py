"""
Pydantic schemas for request/response validation on auth & user routes.
Kept separate from models/ since these represent API contracts,
not database document shapes.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserRegisterSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)
    monthly_income: float = Field(default=0.0, ge=0)
    currency: str = "INR"


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    monthly_income: Optional[float] = Field(default=None, ge=0)
    currency: Optional[str] = None


class UserResponseSchema(BaseModel):
    id: str
    name: str
    email: EmailStr
    monthly_income: float
    currency: str
    created_at: datetime


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponseSchema


class PasswordChangeSchema(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=6, max_length=128)
