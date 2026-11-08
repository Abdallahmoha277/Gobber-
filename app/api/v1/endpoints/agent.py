from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.agents.graph import graph
from app.api.v1.endpoints.auth import oauth2_scheme

router = APIRouter()

class UserRequest(BaseModel):
    query: str

@router.post("/ask")
def ask_agent(request: UserRequest, token: str = Depends(oauth2_scheme)):
    initial_state = {
        "query": request.query, 
        "route": "", 
        "memory": "", 
        "code": "", 
        "stdout": "", 
        "stderr": "", 
        "is_valid": False, 
        "feedback": "", 
        "retries": 0, 
        "response": ""
    }
    result = graph.invoke(initial_state)
    
    # إذا كان الطلب برمجياً
    if result["route"] == "code":
        final_output = result["stdout"] if result["is_valid"] else result["stderr"]
        return {
            "query": request.query,
            "detected_route": result["route"],
            "memory_used": bool(result.get("memory")),
            "is_valid": result["is_valid"],
            "retries": result["retries"],
            "code": result["code"],
            "output": final_output
        }
    # إذا كان الطلب سؤالاً عاماً (QA)
    else:
        return {
            "query": request.query,
            "detected_route": result["route"],
            "memory_used": bool(result.get("memory")),
            "is_valid": True,
            "retries": 0,
            "code": "",
            "output": result.get("response", "No response generated.")
        }