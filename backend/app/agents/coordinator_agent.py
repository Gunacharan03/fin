"""
Coordinator Agent — orchestrates the other agents using LangGraph.

This builds a simple sequential graph:
    expense_agent -> savings_agent -> goal_agent -> reminder_agent -> advisor_agent -> END

Each node enriches a shared state dict. This is what the "AI Insights" page
calls to get a single combined report in one request, instead of the
frontend making 5 separate calls.
"""
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END

from app.agents import expense_agent, savings_agent, goal_agent, reminder_agent, advisor_agent


class FinanceState(TypedDict):
    user_id: str
    currency: str
    expense_analysis: Optional[dict]
    savings_recommendation: Optional[dict]
    goal_prediction: Optional[dict]
    reminder_alert: Optional[dict]
    advisor_report: Optional[dict]


async def _expense_node(state: FinanceState) -> FinanceState:
    state["expense_analysis"] = await expense_agent.run_expense_analysis(state["user_id"])
    return state


async def _savings_node(state: FinanceState) -> FinanceState:
    state["savings_recommendation"] = await savings_agent.run_savings_agent(
        state["user_id"], state["currency"]
    )
    return state


async def _goal_node(state: FinanceState) -> FinanceState:
    state["goal_prediction"] = await goal_agent.run_goal_agent(state["user_id"], state["currency"])
    return state


async def _reminder_node(state: FinanceState) -> FinanceState:
    state["reminder_alert"] = await reminder_agent.run_reminder_agent(state["user_id"], state["currency"])
    return state


async def _advisor_node(state: FinanceState) -> FinanceState:
    state["advisor_report"] = await advisor_agent.generate_monthly_report(
        state["user_id"], state["currency"]
    )
    return state


def build_finance_graph():
    graph = StateGraph(FinanceState)
    graph.add_node("expense_analysis", _expense_node)
    graph.add_node("savings_recommendation", _savings_node)
    graph.add_node("goal_prediction", _goal_node)
    graph.add_node("reminder_alert", _reminder_node)
    graph.add_node("advisor_report", _advisor_node)

    graph.set_entry_point("expense_analysis")
    graph.add_edge("expense_analysis", "savings_recommendation")
    graph.add_edge("savings_recommendation", "goal_prediction")
    graph.add_edge("goal_prediction", "reminder_alert")
    graph.add_edge("reminder_alert", "advisor_report")
    graph.add_edge("advisor_report", END)

    return graph.compile()


_finance_graph = None


def get_finance_graph():
    global _finance_graph
    if _finance_graph is None:
        _finance_graph = build_finance_graph()
    return _finance_graph


async def run_full_insight_pipeline(user_id: str, currency: str = "₹") -> dict:
    """Runs all agents in sequence via LangGraph and returns the combined state."""
    graph = get_finance_graph()
    initial_state: FinanceState = {
        "user_id": user_id,
        "currency": currency,
        "expense_analysis": None,
        "savings_recommendation": None,
        "goal_prediction": None,
        "reminder_alert": None,
        "advisor_report": None,
    }
    final_state = await graph.ainvoke(initial_state)
    return final_state
