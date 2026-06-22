"""
AI service — thin orchestration layer between routes and agents.
Persists every generated insight to MongoDB so the AI Insights page
has history without recomputing (and so users can see past advice).
"""
from datetime import datetime, timezone
from app.database import get_db
from app.agents import expense_agent, savings_agent, goal_agent, reminder_agent, advisor_agent
from app.agents.coordinator_agent import run_full_insight_pipeline
from app.models.insight_model import insight_doc_to_dict


async def _save_insight(user_id: str, insight_type: str, title: str, content: str, data: dict) -> dict:
    db = get_db()
    doc = {
        "user_id": user_id,
        "type": insight_type,
        "title": title,
        "content": content,
        "data": data,
        "created_at": datetime.now(timezone.utc),
    }
    result = await db.insights.insert_one(doc)
    doc["_id"] = result.inserted_id
    return insight_doc_to_dict(doc)


async def get_expense_analysis(user_id: str) -> dict:
    result = await expense_agent.run_expense_analysis(user_id)
    saved = await _save_insight(
        user_id, "expense_analysis", "Expense Analysis", result["analysis_text"], result
    )
    return saved


async def get_savings_recommendation(user_id: str, currency: str = "₹") -> dict:
    result = await savings_agent.run_savings_agent(user_id, currency)
    saved = await _save_insight(
        user_id, "savings_recommendation", "Savings Recommendation", result["recommendation_text"], result
    )
    return saved


async def get_goal_prediction(user_id: str, currency: str = "₹") -> dict:
    result = await goal_agent.run_goal_agent(user_id, currency)
    saved = await _save_insight(
        user_id, "goal_prediction", "Goal Prediction", result["narrative"], result
    )
    return saved


async def get_reminder_alert(user_id: str, currency: str = "₹") -> dict:
    result = await reminder_agent.run_reminder_agent(user_id, currency)
    saved = await _save_insight(
        user_id, "reminder_alert", "Reminder Alert", result["narrative"], result
    )
    return saved


async def get_financial_health_score(user_id: str) -> dict:
    return await advisor_agent.get_financial_health_score(user_id)


async def get_monthly_report(user_id: str, currency: str = "₹") -> dict:
    result = await advisor_agent.generate_monthly_report(user_id, currency)
    saved = await _save_insight(
        user_id, "monthly_report", "Monthly Financial Report", result["report_text"], result
    )
    return saved


async def get_chat_response(user_id: str, message: str, currency: str = "₹") -> dict:
    reply = await advisor_agent.chat_with_advisor(user_id, message, currency)
    saved = await _save_insight(
        user_id, "chat_response", "Chat", reply, {"user_message": message}
    )
    return saved


async def get_full_insight_pipeline(user_id: str, currency: str = "₹") -> dict:
    """Runs the LangGraph coordinator (all agents in sequence) and saves a combined insight."""
    final_state = await run_full_insight_pipeline(user_id, currency)
    saved = await _save_insight(
        user_id,
        "monthly_report",
        "Full AI Insight Report",
        final_state["advisor_report"]["report_text"] if final_state.get("advisor_report") else "",
        final_state,
    )
    return {**final_state, "saved_insight_id": saved["id"]}


async def get_insight_history(user_id: str, limit: int = 20) -> list:
    db = get_db()
    cursor = db.insights.find({"user_id": user_id}).sort("created_at", -1).limit(limit)
    return [insight_doc_to_dict(doc) async for doc in cursor]
