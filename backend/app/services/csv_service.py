"""
CSV service — parses uploaded bank-statement CSVs into transactions
and auto-categorizes them using keyword matching (fast, free, deterministic).

For ambiguous descriptions, the Expense Agent can later re-categorize
using the LLM, but the bulk of categorization is rule-based on purpose:
keyword matching is instant and doesn't burn API calls on thousands of rows.
"""
import pandas as pd
from datetime import datetime, timezone
from io import BytesIO
from app.database import get_db

# Keyword -> category map. Checked against the lowercased description.
CATEGORY_KEYWORDS = {
    "Food": ["restaurant", "zomato", "swiggy", "cafe", "dining", "food"],
    "Groceries": ["grocery", "supermarket", "bigbasket", "blinkit", "mart"],
    "Rent": ["rent", "landlord", "housing"],
    "Utilities": ["electricity", "water bill", "gas bill", "utility"],
    "Transport": ["uber", "ola", "taxi", "metro", "bus fare"],
    "Fuel": ["petrol", "diesel", "fuel", "gas station"],
    "Shopping": ["amazon", "flipkart", "myntra", "mall", "shopping"],
    "Entertainment": ["netflix", "spotify", "movie", "cinema", "prime video"],
    "Healthcare": ["hospital", "pharmacy", "clinic", "doctor", "medical"],
    "Education": ["tuition", "course", "udemy", "school fee", "college"],
    "EMI": ["emi", "loan installment", "loan payment"],
    "Insurance": ["insurance", "premium"],
    "Subscriptions": ["subscription", "membership"],
    "Travel": ["flight", "airbnb", "hotel", "irctc", "makemytrip"],
    "Salary": ["salary", "payroll"],
    "Freelance": ["freelance", "upwork", "fiverr"],
}

REQUIRED_COLUMNS_VARIANTS = {
    "date": ["date", "transaction date", "txn date"],
    "description": ["description", "narration", "details", "particulars"],
    "amount": ["amount", "amt", "value"],
    "type": ["type", "transaction type", "dr/cr"],
}


def _find_column(columns: list, variants: list) -> str:
    lowered = {c.lower().strip(): c for c in columns}
    for variant in variants:
        if variant in lowered:
            return lowered[variant]
    return None


def auto_categorize(description: str, txn_type: str) -> str:
    desc_lower = (description or "").lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in desc_lower for kw in keywords):
            return category
    return "Other"


def parse_bank_statement_csv(file_bytes: bytes) -> list:
    """
    Parses a CSV/Excel bank statement into a list of normalized transaction
    dicts (not yet saved to DB). Raises ValueError with a clear message
    if required columns can't be found.
    """
    try:
        df = pd.read_csv(BytesIO(file_bytes))
    except Exception:
        df = pd.read_excel(BytesIO(file_bytes))

    df.columns = [str(c).strip() for c in df.columns]

    date_col = _find_column(df.columns, REQUIRED_COLUMNS_VARIANTS["date"])
    desc_col = _find_column(df.columns, REQUIRED_COLUMNS_VARIANTS["description"])
    amount_col = _find_column(df.columns, REQUIRED_COLUMNS_VARIANTS["amount"])
    type_col = _find_column(df.columns, REQUIRED_COLUMNS_VARIANTS["type"])

    if not date_col or not amount_col:
        raise ValueError(
            "Could not find required 'date' and 'amount' columns in the file. "
            f"Found columns: {list(df.columns)}"
        )

    transactions = []
    for _, row in df.iterrows():
        try:
            amount = float(row[amount_col])
        except (ValueError, TypeError):
            continue
        if pd.isna(amount) or amount == 0:
            continue

        # Determine type: explicit column, else sign of amount
        if type_col and not pd.isna(row.get(type_col)):
            raw_type = str(row[type_col]).strip().lower()
            txn_type = "income" if raw_type in ("credit", "cr", "income") else "expense"
        else:
            txn_type = "income" if amount > 0 else "expense"

        description = str(row[desc_col]) if desc_col and not pd.isna(row.get(desc_col)) else ""

        try:
            date_val = pd.to_datetime(row[date_col]).to_pydatetime()
            if date_val.tzinfo is None:
                date_val = date_val.replace(tzinfo=timezone.utc)
        except Exception:
            continue

        transactions.append({
            "type": txn_type,
            "amount": abs(amount),
            "category": auto_categorize(description, txn_type),
            "description": description[:200],
            "date": date_val,
            "is_recurring": False,
            "source": "csv_upload",
            "created_at": datetime.now(timezone.utc),
        })

    return transactions


async def save_transactions(user_id: str, transactions: list) -> int:
    if not transactions:
        return 0
    db = get_db()
    for txn in transactions:
        txn["user_id"] = user_id
    result = await db.transactions.insert_many(transactions)
    return len(result.inserted_ids)
