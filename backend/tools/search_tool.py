from tavily import TavilyClient
from langsmith import traceable
from backend.config import TAVILY_API_KEY

client = TavilyClient(api_key=TAVILY_API_KEY)

@traceable(name="search_tool")
def run_search_tool(query: str):
    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=5
    )

    results = []

    for r in response["results"]:
        title = r.get("title", "No title")
        content = r.get("content", "")
        url = r.get("url", "")

        short_content = content[:120] + "..." if len(content) > 120 else content

        results.append({
            "title": title,
            "content": short_content,
            "url": url
        })

    return results