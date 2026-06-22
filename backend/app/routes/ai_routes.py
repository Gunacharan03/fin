"""
AI routes — expose each agent (and the full LangGraph pipeline) via the API.
"""
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field

from app.auth.jwt_handler import get_current_user
from app.services import ai_service

router = APIRouter(prefix="/api/ai", tags=["AI Agents"])


class ChatMessageSchema(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)


@router.get("/expense-analysis")
async def expense_analysis(current_user: dict = Depends(get_current_user)):
    """Runs the Expense Analysis Agent."""
    return await ai_service.get_expense_analysis(str(current_user["_id"]))


@router.get("/savings-recommendation")
async def savings_recommendation(current_user: dict = Depends(get_current_user)):
    """Runs the Savings Agent."""
    return await ai_service.get_savings_recommendation(
        str(current_user["_id"]), current_user.get("currency", "₹")
    )


@router.get("/goal-prediction")
async def goal_prediction(current_user: dict = Depends(get_current_user)):
    """Runs the Goal Agent across all active goals."""
    return await ai_service.get_goal_prediction(
        str(current_user["_id"]), current_user.get("currency", "₹")
    )


@router.get("/reminder-alert")
async def reminder_alert(current_user: dict = Depends(get_current_user)):
    """Runs the Reminder Agent."""
    return await ai_service.get_reminder_alert(
        str(current_user["_id"]), current_user.get("currency", "₹")
    )


@router.get("/financial-health-score")
async def financial_health_score(current_user: dict = Depends(get_current_user)):
    """Returns the deterministic 0-100 financial health score."""
    return await ai_service.get_financial_health_score(str(current_user["_id"]))


@router.get("/monthly-report")
async def monthly_report(current_user: dict = Depends(get_current_user)):
    """Runs the Financial Advisor Agent to generate a monthly report."""
    return await ai_service.get_monthly_report(
        str(current_user["_id"]), current_user.get("currency", "₹")
    )


@router.post("/chat")
async def chat(payload: ChatMessageSchema, current_user: dict = Depends(get_current_user)):
    """Freeform chat with the Financial Advisor Agent, grounded in real user data."""
    return await ai_service.get_chat_response(
        str(current_user["_id"]), payload.message, current_user.get("currency", "₹")
    )


@router.get("/full-report")
async def full_report(current_user: dict = Depends(get_current_user)):
    """
    Runs the full LangGraph coordinator pipeline: expense -> savings -> goal
    -> reminder -> advisor, all in one call. Used by the main AI Insights page.
    """
    return await ai_service.get_full_insight_pipeline(
        str(current_user["_id"]), current_user.get("currency", "₹")
    )


@router.get("/history")
async def insight_history(
    limit: int = Query(default=20, le=100),
    current_user: dict = Depends(get_current_user),
):
    """Returns past AI-generated insights for this user."""
    items = await ai_service.get_insight_history(str(current_user["_id"]), limit)
    return {"items": items, "total": len(items)}
