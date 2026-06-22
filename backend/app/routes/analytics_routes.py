"""
Analytics routes — dashboard summary, category breakdown, monthly trend.
"""
from fastapi import APIRouter, Depends, Query
from datetime import datetime
from typing import Optional

from app.auth.jwt_handler import get_current_user
from app.services import analytics_service

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/summary")
async def summary(
    start_date: Optional[datetime] = Query(default=None),
    end_date: Optional[datetime] = Query(default=None),
    current_user: dict = Depends(get_current_user),
):
    return await analytics_service.get_summary(str(current_user["_id"]), start_date, end_date)


@router.get("/category-breakdown")
async def category_breakdown(
    type: str = Query(default="expense", pattern="^(income|expense)$"),
    current_user: dict = Depends(get_current_user),
):
    return await analytics_service.get_category_breakdown(str(current_user["_id"]), type)


@router.get("/monthly-trend")
async def monthly_trend(
    months: int = Query(default=6, ge=1, le=24),
    current_user: dict = Depends(get_current_user),
):
    return await analytics_service.get_monthly_trend(str(current_user["_id"]), months)


@router.get("/dashboard")
async def dashboard(current_user: dict = Depends(get_current_user)):
    """Combined payload for the main dashboard page (fewer round trips)."""
    user_id = str(current_user["_id"])
    summary_data = await analytics_service.get_summary(user_id)
    category_data = await analytics_service.get_category_breakdown(user_id, "expense")
    trend_data = await analytics_service.get_monthly_trend(user_id, 6)
    recent = await analytics_service.get_recent_transactions(user_id, 8)

    return {
        "summary": summary_data,
        "category_breakdown": category_data,
        "monthly_trend": trend_data,
        "recent_transactions": recent,
    }
