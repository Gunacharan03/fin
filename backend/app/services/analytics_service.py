"""
Analytics service — pure data-aggregation logic (no AI calls here).
Used by analytics_routes.py and by agents that need raw numbers
(e.g. savings_agent, advisor_agent) before reasoning over them.
"""
from datetime import datetime, timezone, timedelta
from collections import defaultdict
from app.database import get_db
from app.utils.helpers import calculate_financial_health_score


async def get_summary(user_id: str, start_date: datetime = None, end_date: datetime = None) -> dict:
    """Total income, expense, and net savings for a date range (all-time if not given)."""
    db = get_db()
    query = {"user_id": user_id}
    if start_date or end_date:
        query["date"] = {}
        if start_date:
            query["date"]["$gte"] = start_date
        if end_date:
            query["date"]["$lte"] = end_date

    total_income = 0.0
    total_expense = 0.0
    async for txn in db.transactions.find(query):
        if txn["type"] == "income":
            total_income += txn["amount"]
        else:
            total_expense += txn["amount"]

    net_savings = total_income - total_expense
    overdue_count = await db.reminders.count_documents({"user_id": user_id, "status": "overdue"})
    health_score = calculate_financial_health_score(total_income, total_expense, net_savings, overdue_count)

    return {
        "total_income": round(total_income, 2),
        "total_expense": round(total_expense, 2),
        "net_savings": round(net_savings, 2),
        "savings_rate_percent": round((net_savings / total_income) * 100, 2) if total_income else 0.0,
        "financial_health_score": health_score,
    }


async def get_category_breakdown(user_id: str, type_filter: str = "expense") -> list:
    """Spend (or income) grouped by category, sorted descending."""
    db = get_db()
    pipeline = [
        {"$match": {"user_id": user_id, "type": type_filter}},
        {"$group": {"_id": "$category", "total": {"$sum": "$amount"}, "count": {"$sum": 1}}},
        {"$sort": {"total": -1}},
    ]
    results = []
    async for doc in db.transactions.aggregate(pipeline):
        results.append({"category": doc["_id"], "total": round(doc["total"], 2), "count": doc["count"]})
    return results


async def get_monthly_trend(user_id: str, months: int = 6) -> list:
    """Income vs expense totals per month, for the last N months."""
    db = get_db()
    now = datetime.now(timezone.utc)
    start = (now.replace(day=1) - timedelta(days=30 * months)).replace(day=1)

    pipeline = [
        {"$match": {"user_id": user_id, "date": {"$gte": start}}},
        {"$group": {
            "_id": {
                "year": {"$year": "$date"},
                "month": {"$month": "$date"},
                "type": "$type",
            },
            "total": {"$sum": "$amount"},
        }},
    ]

    monthly = defaultdict(lambda: {"income": 0.0, "expense": 0.0})
    async for doc in db.transactions.aggregate(pipeline):
        key = f"{doc['_id']['year']}-{doc['_id']['month']:02d}"
        monthly[key][doc["_id"]["type"]] = round(doc["total"], 2)

    return [
        {"month": k, "income": v["income"], "expense": v["expense"], "net": round(v["income"] - v["expense"], 2)}
        for k, v in sorted(monthly.items())
    ]


async def get_recent_transactions(user_id: str, limit: int = 10) -> list:
    db = get_db()
    cursor = db.transactions.find({"user_id": user_id}).sort("date", -1).limit(limit)
    from app.models.transaction_model import transaction_doc_to_dict
    return [transaction_doc_to_dict(doc) async for doc in cursor]
