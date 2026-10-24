from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text, nullable=False)
    solution = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
