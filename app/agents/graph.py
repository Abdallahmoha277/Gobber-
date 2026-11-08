from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from app.agents.router_agent import route_query
from app.agents.responder_agent import generate_response
from app.agents.coder_agent import generate_code
from app.agents.executor_agent import execute_code
from app.agents.critic_agent import evaluate_code
from app.services.memory_service import search_memory, save_memory

class AgentState(TypedDict):
    query: str
    route: str
    memory: str
    code: str
    stdout: str
    stderr: str
    is_valid: bool
    feedback: str
    retries: int
    response: str

def router_node(state: AgentState):
    return {"route": route_query(state["query"])}

def memory_node(state: AgentState):
    memory = search_memory(state["query"])
    return {"memory": memory}

def responder_node(state: AgentState):
    return {"response": generate_response(state["query"])}

def coder_node(state: AgentState):
    code = generate_code(state["query"], state.get("memory", ""), state.get("feedback", ""))
    clean_code = code.replace("```python", "").replace("```", "").strip()
    return {"code": clean_code}

def executor_node(state: AgentState):
    stdout, stderr = execute_code(state["code"])
    return {"stdout": stdout, "stderr": stderr}

def critic_node(state: AgentState):
    output = state["stdout"] if not state["stderr"] else state["stderr"]
    is_valid, feedback = evaluate_code(state["query"], state["code"], output)
    
    if is_valid:
        save_memory(state["query"], state["code"])
        
    return {
        "is_valid": is_valid, 
        "feedback": feedback, 
        "retries": state.get("retries", 0) + 1
    }

def route_decision(state: AgentState) -> Literal["memory", "responder"]:
    return "memory" if state["route"] == "code" else "responder"

def check_critic(state: AgentState) -> Literal["coder", "end"]:
    if state["is_valid"] or state["retries"] >= 3:
        return "end"
    return "coder"

workflow = StateGraph(AgentState)
workflow.add_node("router", router_node)
workflow.add_node("memory", memory_node)
workflow.add_node("responder", responder_node)
workflow.add_node("coder", coder_node)
workflow.add_node("executor", executor_node)
workflow.add_node("critic", critic_node)

workflow.set_entry_point("router")
workflow.add_conditional_edges("router", route_decision)

workflow.add_edge("memory", "coder")
workflow.add_edge("coder", "executor")
workflow.add_edge("executor", "critic")
workflow.add_conditional_edges("critic", check_critic, {"coder": "coder", "end": END})
workflow.add_edge("responder", END)

graph = workflow.compile()