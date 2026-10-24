from app.agents.router_agent import route_query

queries = [
    "What is the capital of France?",
    "Find the latest news about AI.",
    "Write a Python function to sort a list.",
]

for q in queries:
    print(f"Query: {q}")
    print(f"Routed to: {route_query(q)}\n")
