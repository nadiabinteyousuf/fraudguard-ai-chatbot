from langsmith import traceable
from .router_agent import route_query
from .fraud_agent import run_fraud_agent
from .search_agent import run_search_agent
from .rag_agent import run_rag_agent
from .ocr_agent import run_ocr_agent
from backend.tools.search_tool import run_search_tool

@traceable(name="main_agent")
def run_main_agent(query: str, uploaded_file=None):
    route = route_query(query)

    if route == "SEARCH_AGENT":
        results = run_search_tool(query)
        reply = run_search_agent(query, results)

        return {
            "reply": reply,
            "risk": "LOW",
            "score": 30
        }

    elif route == "FRAUD_AGENT":
        return run_fraud_agent(query)

    elif route == "OCR_AGENT":
        if uploaded_file:
            return run_ocr_agent(uploaded_file, query)

        return {
            "reply": "Please upload a document to analyze.",
            "risk": "LOW",
            "score": 0
        }

    elif route == "RAG_AGENT":
        return run_rag_agent(query)

    return {
        "reply": "Unable to process request.",
        "risk": "LOW",
        "score": 10
    }