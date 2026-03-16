from langsmith import traceable
from backend.rag.vector_store import load_vector_store

@traceable(name="rag_agent")
def run_rag_agent(query: str):
    vectorstore = load_vector_store()
    docs = vectorstore.similarity_search(query, k=2)

    if not docs:
        return {
            "reply": "No relevant information found in the knowledge base.",
            "risk": "LOW",
            "score": 20
        }

    context = "\n\n".join([doc.page_content for doc in docs])

    return {
        "reply": context,
        "risk": "LOW",
        "score": 20
    }