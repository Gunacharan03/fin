"""
Expense Analysis Agent.

Responsibilities (per project spec):
- Analyze transactions
- Find spending trends
- Detect unusual expenses

Design note: the heavy numeric aggregation (totals, category sums) is done
in plain Python/Mongo (cheap, deterministic) — the LLM is only used for the
*narrative interpretation* of those numbers. This keeps Gemini API calls cheap
and avoids asking a language model to do arithmetic it might get wrong.
"""
from app.config.ai_config import get_llm
from app.services import analytics_service
from langchain_core.messages import SystemMessage, HumanMessage
import statistics


async def detect_unusual_expenses(user_id: str) -> list:
    """
    Flags transactions that are statistically unusual for their category
    (> 1.5x the category's average), using plain stats — no LLM needed.
    """
    from app.database import get_db
    db = get_db()

    category_amounts = {}
    async for txn in db.transactions.find({"user_id": user_id, "type": "expense"}):
        category_amounts.setdefault(txn["category"], []).append(txn)

    unusual = []
    for category, txns in category_amounts.items():
        amounts = [t["amount"] for t in txns]
        if len(amounts) < 3:
            continue
        avg = statistics.mean(amounts)
        for t in txns:
            if t["amount"] > avg * 1.5:
                unusual.append({
                    "id": str(t["_id"]),
                    "category": category,
                    "amount": t["amount"],
                    "average_for_category": round(avg, 2),
                    "description": t.get("description", ""),
                    "date": t["date"].isoformat() if hasattr(t["date"], "isoformat") else str(t["date"]),
                })
    return sorted(unusual, key=lambda x: x["amount"], reverse=True)[:10]


async def run_expense_analysis(user_id: str) -> dict:
    """
    Full expense agent run: gathers spending data, computes trends/anomalies,
    then asks the LLM to write a short, plain-language analysis.
    """
    summary = await analytics_service.get_summary(user_id)
    breakdown = await analytics_service.get_category_breakdown(user_id, "expense")
    trend = await analytics_service.get_monthly_trend(user_id, 3)
    unusual = await detect_unusual_expenses(user_id)

    top_categories = breakdown[:5]

    llm = get_llm(temperature=0.3)
    system_prompt = (
        "You are the Expense Analysis Agent inside a personal finance app. "
        "You write short, clear, encouraging analyses of a user's spending data. "
        "Never invent numbers — only use the numbers given to you. "
        "Keep your response under 150 words, in plain language, no jargon. "
        "Use a friendly but professional tone. Format with short paragraphs or "
        "a brief bullet list where helpful."
    )
    human_prompt = (
        f"Here is the user's financial data:\n"
        f"- Total income: {summary['total_income']}\n"
        f"- Total expense: {summary['total_expense']}\n"
        f"- Net savings: {summary['net_savings']}\n"
        f"- Top spending categories: {top_categories}\n"
        f"- Monthly trend (last 3 months): {trend}\n"
        f"- Unusually large transactions detected: {unusual[:5]}\n\n"
        "Write a brief expense analysis highlighting the biggest spending "
        "category, any concerning trends, and one specific observation about "
        "unusual transactions (if any)."
    )

    response = await llm.ainvoke([SystemMessage(content=system_prompt), HumanMessage(content=human_prompt)])

    return {
        "analysis_text": response.content,
        "top_categories": top_categories,
        "unusual_expenses": unusual,
        "monthly_trend": trend,
    }
