"""
Savings Agent.

Responsibilities (per project spec):
- Calculate possible savings
- Recommend budget allocation

Example target output (from spec):
    "You spent ₹6000 on food. Reducing food expenses by 15% can save ₹900 monthly."
"""
from app.config.ai_config import get_llm
from app.services import analytics_service
from langchain_core.messages import SystemMessage, HumanMessage

# Suggested reduction percentage by category — categories not listed default to 10%.
# These are deliberately conservative (easy wins) vs. essentials like Rent/EMI.
REDUCTION_SUGGESTIONS = {
    "Food": 0.15, "Entertainment": 0.25, "Shopping": 0.20,
    "Subscriptions": 0.30, "Transport": 0.10, "Travel": 0.20,
}
NON_REDUCIBLE = {"Rent", "EMI", "Insurance", "Healthcare", "Education"}


async def calculate_savings_opportunities(user_id: str, currency: str = "₹") -> list:
    """Rule-based calculation of potential monthly savings per category."""
    breakdown = await analytics_service.get_category_breakdown(user_id, "expense")
    opportunities = []

    for entry in breakdown:
        category = entry["category"]
        if category in NON_REDUCIBLE:
            continue
        reduction_pct = REDUCTION_SUGGESTIONS.get(category, 0.10)
        potential_saving = round(entry["total"] * reduction_pct, 2)
        if potential_saving < 50:  # not worth surfacing tiny amounts
            continue
        opportunities.append({
            "category": category,
            "current_spend": entry["total"],
            "suggested_reduction_percent": int(reduction_pct * 100),
            "potential_monthly_saving": potential_saving,
            "message": (
                f"You spent {currency}{entry['total']:.0f} on {category}. "
                f"Reducing {category.lower()} expenses by {int(reduction_pct * 100)}% "
                f"can save {currency}{potential_saving:.0f} monthly."
            ),
        })

    return sorted(opportunities, key=lambda x: x["potential_monthly_saving"], reverse=True)


async def run_savings_agent(user_id: str, currency: str = "₹") -> dict:
    """Computes savings opportunities, then asks the LLM for a prioritized recommendation."""
    opportunities = await calculate_savings_opportunities(user_id, currency)
    summary = await analytics_service.get_summary(user_id)

    total_potential = round(sum(o["potential_monthly_saving"] for o in opportunities), 2)

    llm = get_llm(temperature=0.3)
    system_prompt = (
        "You are the Savings Agent inside a personal finance app. "
        "Given a list of pre-calculated savings opportunities, recommend which "
        "1-3 changes the user should prioritize first, and why. Be specific and "
        "encouraging, not preachy. Under 120 words. Never invent numbers beyond "
        "what's given."
    )
    human_prompt = (
        f"Current savings rate: {summary['savings_rate_percent']}%\n"
        f"Savings opportunities found: {opportunities}\n"
        f"Total potential monthly savings if all suggestions are followed: {currency}{total_potential}\n\n"
        "Recommend which 1-3 opportunities to prioritize first and explain why briefly."
    )
    response = await llm.ainvoke([SystemMessage(content=system_prompt), HumanMessage(content=human_prompt)])

    return {
        "recommendation_text": response.content,
        "opportunities": opportunities,
        "total_potential_monthly_saving": total_potential,
    }
