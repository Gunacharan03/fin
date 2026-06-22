"""
Google Gemini client configuration shared across all LangGraph agents.

All agent files import `get_llm()` from here, so this is the only file
that needs to change if the LLM provider is swapped again later.
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config.settings import settings


def get_llm(temperature: float = 0.3) -> ChatGoogleGenerativeAI:
    """
    Returns a configured LangChain ChatGoogleGenerativeAI instance used by every agent.

    temperature is kept low (0.2-0.4) by default for financial advice —
    we want consistent, grounded answers, not creative ones.
    """
    return ChatGoogleGenerativeAI(
        model=settings.GEMINI_MODEL,
        google_api_key=settings.GEMINI_API_KEY,
        temperature=temperature,
    )
