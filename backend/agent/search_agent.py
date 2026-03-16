from langsmith import traceable

@traceable(name="search_agent")
def run_search_agent(query: str, results: list):
    if not results:
        return f"No internet search results found for: {query}"

    formatted_results = []

    for i, item in enumerate(results, start=1):
        formatted_results.append(
            f"""**{i}. {item['title']}**

{item['content']}

Source: {item['url']}
"""
        )

    answer = f"""
Internet Search Results for: **{query}**

{chr(10).join(formatted_results)}
"""

    return answer.strip()