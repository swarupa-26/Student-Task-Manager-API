from sqlalchemy import Column, String, Date, DateTime
from sqlalchemy.sql import func
from ..db.base import Base
import enum

class StatusEnum(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True)
    title = Column(String(120), nullable=False, index=True)
    description = Column(String(500), nullable=True)
    status = Column(String(50), nullable=False, default=StatusEnum.pending.value)
    due_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
