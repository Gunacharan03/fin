"""
General-purpose helper functions used across routes/services.
"""
from datetime import datetime, timezone
from bson import ObjectId
from typing import Any, Dict, List


def is_valid_object_id(id_str: str) -> bool:
    return ObjectId.is_valid(id_str)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def month_bounds(year: int, month: int) -> tuple:
    """Return (start, end) datetimes for the given month (UTC)."""
    start = datetime(year, month, 1, tzinfo=timezone.utc)
    if month == 12:
        end = datetime(year + 1, 1, 1, tzinfo=timezone.utc)
    else:
        end = datetime(year, month + 1, 1, tzinfo=timezone.utc)
    return start, end


def calculate_financial_health_score(
    total_income: float,
    total_expense: float,
    total_savings: float,
    overdue_reminders: int,
) -> int:
    """
    Simple, explainable heuristic score (0-100) combining:
    - savings rate (50% weight)
    - spending ratio (30% weight)
    - bill discipline (20% weight)

    This is intentionally rule-based (not LLM-based) so it's fast,
    deterministic, and free to compute on every dashboard load.
    The Advisor Agent can reference this score in its narrative output.
    """
    if total_income <= 0:
        return 0

    savings_rate = max(0, total_savings) / total_income
    savings_score = min(savings_rate * 100, 100) * 0.5

    spend_ratio = total_expense / total_income if total_income else 1
    spend_score = max(0, (1 - spend_ratio)) * 100 * 0.3

    bill_score = max(0, 100 - (overdue_reminders * 20)) * 0.2

    score = round(savings_score + spend_score + bill_score)
    return max(0, min(100, score))


def paginate(items: List[Any], page: int = 1, page_size: int = 20) -> Dict[str, Any]:
    start = (page - 1) * page_size
    end = start + page_size
    return {
        "items": items[start:end],
        "page": page,
        "page_size": page_size,
        "total": len(items),
        "total_pages": max(1, (len(items) + page_size - 1) // page_size),
    }
