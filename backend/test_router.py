import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.agent.router_agent import route_query

queries = [
    "latest cyber fraud attacks",
    "what is AML structuring",
    "analyze this suspicious transaction of $450 repeated 12 times",
    "extract text from this invoice"
]

for q in queries:
    print("Query:", q)
    print("Route:", route_query(q))
    print("-" * 40)