from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal


class TransactionCreateSchema(BaseModel):
    type: Literal["income", "expense"]
    amount: float = Field(..., gt=0)
    category: str
    description: Optional[str] = ""
    date: datetime
    is_recurring: bool = False


class TransactionUpdateSchema(BaseModel):
    type: Optional[Literal["income", "expense"]] = None
    amount: Optional[float] = Field(default=None, gt=0)
    category: Optional[str] = None
    description: Optional[str] = None
    date: Optional[datetime] = None
    is_recurring: Optional[bool] = None


class TransactionResponseSchema(BaseModel):
    id: str
    user_id: str
    type: str
    amount: float
    category: str
    description: str
    date: datetime
    is_recurring: bool
    source: str
    created_at: datetime


class TransactionFilterSchema(BaseModel):
    type: Optional[Literal["income", "expense"]] = None
    category: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
