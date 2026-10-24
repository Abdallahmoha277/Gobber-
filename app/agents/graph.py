from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from app.agents.router_agent import route_query
from app.agents.responder_agent import generate_response
from app.agents.coder_agent import generate_code
from app.agents.executor_agent import execute_code
from app.services.memory_service import search_memory, save_memory


class AgentState(TypedDict):
    query: str
    route: str
    memory: str
    code: str
    stdout: str
    stderr: str
    response: str


def router_node(state: AgentState):
    return {"route": route_query(state["query"])}


def memory_node(state: AgentState):
    memory = search_memory(state["query"])
    return {"memory": memory}


def responder_node(state: AgentState):
    return {"response": generate_response(state["query"])}


def coder_node(state: AgentState):
    code = generate_code(state["query"], state.get("memory", ""))
    clean_code = code.replace("```python", "").replace("```", "").strip()
    save_memory(state["query"], clean_code)
    return {"code": clean_code}


def executor_node(state: AgentState):
    stdout, stderr = execute_code(state["code"])
    final_response = f"Code:\n{state['code']}\n\nOutput:\n{stdout}\n\nErrors:\n{stderr}"
    return {"stdout": stdout, "stderr": stderr, "response": final_response}


def route_decision(state: AgentState) -> Literal["memory", "responder"]:
    return "memory" if state["route"] == "code" else "responder"


workflow = StateGraph(AgentState)
workflow.add_node("router", router_node)
workflow.add_node("memory", memory_node)
workflow.add_node("responder", responder_node)
workflow.add_node("coder", coder_node)
workflow.add_node("executor", executor_node)

workflow.set_entry_point("router")
workflow.add_conditional_edges("router", route_decision)

workflow.add_edge("memory", "coder")
workflow.add_edge("coder", "executor")
workflow.add_edge("executor", END)
workflow.add_edge("responder", END)

graph = workflow.compile()
