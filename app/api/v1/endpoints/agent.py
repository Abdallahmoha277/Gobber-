from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.agents.graph import graph
from app.api.v1.endpoints.auth import oauth2_scheme

router = APIRouter()


class UserRequest(BaseModel):
    query: str


@router.post("/ask")
def ask_agent(request: UserRequest, token: str = Depends(oauth2_scheme)):
    initial_state = {"query": request.query, "route": "", "memory": "", "response": ""}
    result = graph.invoke(initial_state)

    return {
        "query": request.query,
        "detected_route": result["route"],
        "memory_used": bool(result.get("memory")),
        "response": result["response"],
    }
