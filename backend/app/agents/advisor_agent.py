"""
Financial Advisor Agent.

Responsibilities (per project spec):
- Personalized advice
- Monthly reports
- Financial health score
- (also powers the freeform finance chatbot)
"""
from app.config.ai_config import get_llm
from app.services import analytics_service
from app.agents.reminder_agent import get_due_and_overdue
from langchain_core.messages import SystemMessage, HumanMessage
from app.database import get_db


async def get_financial_health_score(user_id: str) -> dict:
    """Returns the deterministic 0-100 score plus the inputs that produced it."""
    summary = await analytics_service.get_summary(user_id)
    return {
        "score": summary["financial_health_score"],
        "savings_rate_percent": summary["savings_rate_percent"],
        "total_income": summary["total_income"],
        "total_expense": summary["total_expense"],
        "net_savings": summary["net_savings"],
    }


async def generate_monthly_report(user_id: str, currency: str = "₹") -> dict:
    """Full monthly report: numbers + LLM narrative."""
    summary = await analytics_service.get_summary(user_id)
    breakdown = await analytics_service.get_category_breakdown(user_id, "expense")
    trend = await analytics_service.get_monthly_trend(user_id, 1)
    reminders = await get_due_and_overdue(user_id)

    db = get_db()
    goals_count = await db.goals.count_documents({"user_id": user_id, "status": "active"})
    completed_goals = await db.goals.count_documents({"user_id": user_id, "status": "completed"})

    llm = get_llm(temperature=0.4)
    system_prompt = (
        "You are the Financial Advisor Agent inside a personal finance app. "
        "Write a friendly monthly financial report (under 200 words) covering: "
        "overall financial health, top spending area, savings performance, and "
        "one specific actionable tip for next month. Use the financial health "
        "score to frame your tone (above 70 = encouraging, 40-70 = constructive, "
        "below 40 = supportive but direct about the need for change). "
        "Never invent numbers."
    )
    human_prompt = (
        f"Financial health score: {summary['financial_health_score']}/100\n"
        f"Total income: {currency}{summary['total_income']}\n"
        f"Total expense: {currency}{summary['total_expense']}\n"
        f"Net savings: {currency}{summary['net_savings']} ({summary['savings_rate_percent']}%)\n"
        f"Top expense categories: {breakdown[:5]}\n"
        f"Active goals: {goals_count}, Completed goals: {completed_goals}\n"
        f"Overdue bills: {len(reminders['overdue'])}\n\n"
        "Write the monthly report now."
    )
    response = await llm.ainvoke([SystemMessage(content=system_prompt), HumanMessage(content=human_prompt)])

    return {
        "report_text": response.content,
        "financial_health_score": summary["financial_health_score"],
        "summary": summary,
        "top_categories": breakdown[:5],
        "goals_count": goals_count,
        "completed_goals": completed_goals,
        "overdue_bills": len(reminders["overdue"]),
    }


async def chat_with_advisor(user_id: str, user_message: str, currency: str = "₹") -> str:
    """
    Powers the chatbot page. Pulls the user's current financial context
    so the advisor can answer questions like "can I afford a 20k purchase?"
    grounded in real data rather than generic advice.
    """
    summary = await analytics_service.get_summary(user_id)
    breakdown = await analytics_service.get_category_breakdown(user_id, "expense")

    db = get_db()
    goals_cursor = db.goals.find({"user_id": user_id, "status": "active"})
    goals = [{"title": g["title"], "target": g["target_amount"], "current": g.get("current_amount", 0)}
              async for g in goals_cursor]

    llm = get_llm(temperature=0.5)
    system_prompt = (
        "You are a helpful, friendly personal finance advisor chatbot inside a "
        "budgeting app. You have access to the user's real financial summary below — "
        "ground your answers in it whenever relevant. Keep answers concise and practical. "
        "Do not give specific investment/stock picks or legal/tax advice — suggest "
        "consulting a licensed professional for those. Never invent numbers not given to you."
    )
    human_prompt = (
        f"User's financial context:\n"
        f"- Total income: {currency}{summary['total_income']}\n"
        f"- Total expense: {currency}{summary['total_expense']}\n"
        f"- Net savings: {currency}{summary['net_savings']}\n"
        f"- Top expense categories: {breakdown[:5]}\n"
        f"- Active goals: {goals}\n\n"
        f"User's question: {user_message}"
    )
    response = await llm.ainvoke([SystemMessage(content=system_prompt), HumanMessage(content=human_prompt)])
    return response.content
