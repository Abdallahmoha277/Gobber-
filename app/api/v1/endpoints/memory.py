from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.memory import Memory
from app.schemas.memory import MemoryCreate, MemoryResponse

router = APIRouter()


@router.post("/", response_model=MemoryResponse, status_code=201)
def create_memory(memory_in: MemoryCreate, db: Session = Depends(get_db)):
    db_memory = Memory(query=memory_in.query, solution=memory_in.solution)
    db.add(db_memory)
    db.commit()
    db.refresh(db_memory)
    return db_memory


@router.get("/", response_model=List[MemoryResponse])
def read_memories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Memory).offset(skip).limit(limit).all()
