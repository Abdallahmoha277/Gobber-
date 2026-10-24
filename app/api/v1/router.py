from fastapi import APIRouter
from app.api.v1.endpoints import health, memory, agent, auth

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(memory.router, prefix="/memories", tags=["Memories"])
api_router.include_router(agent.router, prefix="/agent", tags=["Agent"])
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
