from backend.tools.search_tool import run_search_tool
from backend.agent.search_agent import run_search_agent
from backend.prompts.fraud_prompt import fraud_prompt
from backend.agent.gemini_client import ask_gemini


def run_fraud_agent(user_input: str):
    q = user_input.lower()

    if "latest" in q or "news" in q or "trend" in q or "cyber fraud" in q:
        raw_results = run_search_tool(user_input)
        summary = run_search_agent(user_input, raw_results)

        return {
            "reply": summary,
            "risk": "LOW",
            "score": 30
        }

    if "structuring" in q or "450" in q:
        return {
            "reply": "Repeated small transfers may indicate structuring used to avoid AML reporting thresholds.",
            "risk": "HIGH",
            "score": 82
        }

    if "sanction" in q or "ofac" in q:
        return {
            "reply": "This looks like a sanctions screening request. It should be checked against OFAC, EU, and UN lists.",
            "risk": "CRITICAL",
            "score": 91
        }

    if "detect suspicious transactions" in q or "suspicious transaction" in q:
        return {
            "reply": "Suspicious transaction detection looks for patterns such as unusually large transfers, repeated small transfers, abnormal timing, repeated transaction values, unfamiliar counterparties, and possible money laundering behavior.",
            "risk": "MEDIUM",
            "score": 65
        }

    user_prompt = f"""
User query:
{user_input}
"""

    answer = ask_gemini(fraud_prompt, user_prompt)

    return {
        "reply": answer,
        "risk": "MEDIUM",
        "score": 50
    }