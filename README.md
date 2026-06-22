# Fin — AI-Powered Personal Finance Assistant

> "For Every Income, A Smarter Outcome"

A full-stack personal finance app with multi-agent AI insights: track income/expenses,
manage savings goals and EMI reminders, import bank statements, and get AI-generated
financial analysis, savings recommendations, goal predictions, and a chat-based advisor.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React.js (Vite) + Chakra UI + React Router + Axios + Recharts |
| Backend | FastAPI (Python) |
| Database | MongoDB Atlas (via Motor async driver) |
| Auth | JWT (python-jose + passlib/bcrypt) |
| AI / Agents | Google Gemini API + LangGraph + LangChain |
| File processing | Pandas (CSV/Excel bank statement parsing) |

> **Note on stack naming:** the original project brief described this as a "MERN" app,
> but actually specified FastAPI (Python) + MongoDB + Gemini + LangGraph. This build
> uses that exact architecture as specified, including **Google Gemini** as the LLM provider.
> This combination (FastAPI + React + MongoDB) is sometimes called the **FARM stack**.
> It is not literally MERN (Mongo/Express/React/Node) since the backend is Python, not Node.

## Project Structure

```
fin/
├── backend/                  FastAPI application
│   ├── main.py                Entrypoint (uvicorn main:app)
│   ├── requirements.txt
│   ├── .env.example           Copy to .env and fill in real values
│   └── app/
│       ├── config/            Settings + Gemini client config
│       ├── models/            MongoDB document shape definitions
│       ├── schemas/            Pydantic request/response validation
│       ├── routes/            All API endpoints
│       ├── auth/               JWT + password hashing
│       ├── agents/             5 LangGraph agents + coordinator
│       ├── services/           Analytics, CSV parsing, AI orchestration, notifications
│       └── uploads/             Temp storage for uploaded files
│
├── frontend/                  React (Vite) application
│   ├── .env.example            Copy to .env and set VITE_API_BASE_URL
│   └── src/
│       ├── components/          Reusable UI pieces
│       ├── pages/                One file per route
│       ├── services/              Axios calls to the backend
│       ├── context/                Auth + Finance React context
│       └── routes/                  AppRoutes.jsx (all route definitions)
│
└── docs/                      (Add your own SRS/architecture docs here)
```

## Setup Instructions

### 1. Prerequisites
- Python 3.10+
- Node.js 18+
- A MongoDB Atlas cluster (free tier is fine) — [mongodb.com/atlas](https://www.mongodb.com/atlas)
- A Google Gemini API key — [aistudio.google.com/apikey](https://aistudio.google.com/apikey) (free tier available)

### 2. Backend setup

```bash
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Now edit .env and fill in:
#   MONGODB_URI=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/...
#   JWT_SECRET_KEY=<run: python -c "import secrets; print(secrets.token_hex(32))">
#   GEMINI_API_KEY=AIza...

uvicorn main:app --reload --port 8000
```

The API will be live at `http://localhost:8000`. Interactive docs (Swagger UI) at
`http://localhost:8000/docs`.

### 3. Frontend setup

```bash
cd frontend
npm install
cp .env.example .env
# Confirm VITE_API_BASE_URL=http://localhost:8000

npm run dev
```

The app will be live at `http://localhost:5173`.

### 4. First use
1. Open the frontend, click "Create an account", and register.
2. Add a few transactions (Transactions → Add Transaction), or upload a CSV (Import CSV).
3. Create a savings goal (Goals → New Goal) and a bill reminder (Reminders → New Reminder).
4. Visit **AI Insights** and click "Generate insights" — this runs the full LangGraph
   agent pipeline (expense → savings → goal → reminder → advisor) using your Gemini key.
5. Try the **Advisor Chat** page to ask freeform questions grounded in your real data.

## The AI Agents

| Agent | File | What it does |
|---|---|---|
| Expense Analysis Agent | `agents/expense_agent.py` | Finds spending trends, flags statistically unusual transactions |
| Savings Agent | `agents/savings_agent.py` | Calculates category-level savings opportunities and prioritizes them |
| Goal Agent | `agents/goal_agent.py` | Predicts goal completion dates from your actual savings rate |
| Reminder Agent | `agents/reminder_agent.py` | Surfaces overdue and upcoming EMIs/bills as a prioritized alert |
| Financial Advisor Agent | `agents/advisor_agent.py` | Monthly reports, financial health score, and the chatbot |
| Coordinator Agent | `agents/coordinator_agent.py` | LangGraph state machine that runs all 5 agents in sequence |

**Design choice:** all heavy number-crunching (sums, averages, trend math) happens in
plain Python/MongoDB aggregation — the LLM is only used to turn already-correct numbers
into a clear, human-readable narrative. This keeps the app fast, cheap to run, and avoids
asking a language model to do arithmetic it could get wrong.

## API Overview

All endpoints except `/api/auth/register` and `/api/auth/login` require an
`Authorization: Bearer <token>` header.

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/auth/register` | Create account |
| POST | `/api/auth/login` | Get JWT token |
| GET/PUT | `/api/auth/me` | View/update profile |
| POST | `/api/auth/change-password` | Change password |
| GET/POST | `/api/transactions` | List / create transactions |
| PUT/DELETE | `/api/transactions/{id}` | Update / delete a transaction |
| GET/POST | `/api/goals` | List / create goals |
| POST | `/api/goals/{id}/contribute` | Add funds toward a goal |
| GET/POST | `/api/reminders` | List / create reminders |
| POST | `/api/reminders/{id}/mark-paid` | Mark a bill/EMI as paid |
| GET | `/api/analytics/dashboard` | Combined dashboard payload |
| POST | `/api/csv/preview` | Preview a bank statement before import |
| POST | `/api/csv/confirm` | Import a bank statement |
| GET | `/api/ai/full-report` | Run the full LangGraph agent pipeline |
| POST | `/api/ai/chat` | Chat with the Financial Advisor Agent |

Full interactive documentation is auto-generated at `/docs` once the backend is running.

## Notes & Future Enhancements

The `services/notification_service.py` file currently logs notifications to the
console rather than sending real emails/SMS — see the comments in that file for how
to plug in a real provider (SendGrid, Twilio, etc.) when you're ready.

Phase 2 ideas from the original brief (not yet implemented): voice expense entry,
OCR receipt scanning, WhatsApp reminders, investment recommendations, UPI integration,
multi-language support, and credit score analysis.
