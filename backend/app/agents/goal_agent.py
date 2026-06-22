"""
Goal Agent.

Responsibilities (per project spec):
- Track goals
- Predict completion date

Example target output (from spec):
    "Laptop Goal — Target: ₹60,000, Current: ₹30,000.
     At current savings rate, goal can be achieved in 5 months."
"""
from datetime import datetime, timezone, timedelta
from app.database import get_db
from app.services import analytics_service
from app.config.ai_config import get_llm
from langchain_core.messages import SystemMessage, HumanMessage
from app.models.goal_model import goal_doc_to_dict


async def predict_goal_completion(user_id: str, goal: dict) -> dict:
    """
    Rule-based prediction: uses the user's average monthly net savings
    (last 3 months) to estimate months-to-completion for a single goal.
    """
    summary = await analytics_service.get_summary(user_id)
    trend = await analytics_service.get_monthly_trend(user_id, 3)

    monthly_savings_values = [m["net"] for m in trend if m["net"] > 0]
    avg_monthly_savings = (
        sum(monthly_savings_values) / len(monthly_savings_values)
        if monthly_savings_values else 0.0
    )

    remaining = max(0, goal["target_amount"] - goal.get("current_amount", 0.0))

    if remaining <= 0:
        months_needed = 0
    elif avg_monthly_savings <= 0:
        months_needed = None  # can't project — no positive savings trend
    else:
        months_needed = round(remaining / avg_monthly_savings, 1)

    projected_date = None
    if months_needed is not None and months_needed > 0:
        projected_date = (datetime.now(timezone.utc) + timedelta(days=30 * months_needed)).isoformat()

    return {
        "goal_id": str(goal["_id"]),
        "title": goal["title"],
        "target_amount": goal["target_amount"],
        "current_amount": goal.get("current_amount", 0.0),
        "remaining_amount": remaining,
        "avg_monthly_savings": round(avg_monthly_savings, 2),
        "months_needed": months_needed,
        "projected_completion_date": projected_date,
    }


async def run_goal_agent(user_id: str, currency: str = "₹") -> dict:
    """Runs predictions for all active goals, then gets an LLM narrative summary."""
    db = get_db()
    cursor = db.goals.find({"user_id": user_id, "status": "active"})
    goals = [doc async for doc in cursor]

    if not goals:
        return {
            "narrative": "You don't have any active savings goals yet. Create one to get personalized predictions!",
            "predictions": [],
        }

    predictions = [await predict_goal_completion(user_id, g) for g in goals]

    llm = get_llm(temperature=0.3)
    system_prompt = (
        "You are the Goal Agent inside a personal finance app. "
        "Given goal predictions, write a short, motivating summary (under 130 words) "
        "covering: which goal is closest to completion, and a tip for any goal that "
        "lacks a positive savings trend (months_needed is null). Never invent numbers."
    )
    human_prompt = f"Goal predictions:\n{predictions}\n\nWrite the summary now."
    response = await llm.ainvoke([SystemMessage(content=system_prompt), HumanMessage(content=human_prompt)])

    return {"narrative": response.content, "predictions": predictions}
