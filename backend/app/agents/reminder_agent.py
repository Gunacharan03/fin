"""
Reminder Agent.

Responsibilities (per project spec):
- Track EMIs
- Generate reminders
- Notify users

This agent is mostly rule-based (deadlines are facts, not something to
"reason" about) but uses the LLM to produce a friendly, prioritized
natural-language summary of what's due soon and what's overdue.
"""
from datetime import datetime, timezone, timedelta
from app.database import get_db
from app.config.ai_config import get_llm
from langchain_core.messages import SystemMessage, HumanMessage
from app.models.reminder_model import reminder_doc_to_dict


async def get_due_and_overdue(user_id: str, upcoming_days: int = 7) -> dict:
    db = get_db()
    now = datetime.now(timezone.utc)

    # Auto-flag overdue
    await db.reminders.update_many(
        {"user_id": user_id, "status": "pending", "due_date": {"$lt": now}},
        {"$set": {"status": "overdue"}},
    )

    overdue_cursor = db.reminders.find({"user_id": user_id, "status": "overdue"}).sort("due_date", 1)
    overdue = [reminder_doc_to_dict(doc) async for doc in overdue_cursor]

    upcoming_cursor = db.reminders.find({
        "user_id": user_id,
        "status": "pending",
        "due_date": {"$gte": now, "$lte": now + timedelta(days=upcoming_days)},
    }).sort("due_date", 1)
    upcoming = [reminder_doc_to_dict(doc) async for doc in upcoming_cursor]

    return {"overdue": overdue, "upcoming": upcoming}


async def run_reminder_agent(user_id: str, currency: str = "₹") -> dict:
    data = await get_due_and_overdue(user_id)

    if not data["overdue"] and not data["upcoming"]:
        return {
            "narrative": "You're all caught up! No bills or EMIs due soon.",
            "overdue": [],
            "upcoming": [],
        }

    llm = get_llm(temperature=0.2)
    system_prompt = (
        "You are the Reminder Agent inside a personal finance app. "
        "Given overdue and upcoming bills/EMIs, write a short, direct alert "
        "(under 100 words) prioritizing overdue items first, then upcoming ones "
        "by urgency. Be clear and a little urgent for overdue items, calm for upcoming ones."
    )
    human_prompt = (
        f"Overdue: {data['overdue']}\n"
        f"Upcoming (next 7 days): {data['upcoming']}\n\n"
        "Write the alert now."
    )
    response = await llm.ainvoke([SystemMessage(content=system_prompt), HumanMessage(content=human_prompt)])

    return {"narrative": response.content, "overdue": data["overdue"], "upcoming": data["upcoming"]}
