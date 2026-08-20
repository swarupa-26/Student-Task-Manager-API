from pydantic import BaseModel, ConfigDict, constr, field_validator
from typing import Optional
from datetime import date
from enum import Enum

class StatusEnum(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: constr(min_length=1, max_length=120)
    description: Optional[constr(max_length=500)] = None
    due_date: Optional[date] = None
    status: Optional[StatusEnum] = StatusEnum.pending

    @field_validator("status")
    def validate_status_not_null(cls, value):
        if value is None:
            raise ValueError("status cannot be null")
        return value

class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Optional[constr(min_length=1, max_length=120)] = None
    description: Optional[constr(max_length=500)] = None
    due_date: Optional[date] = None
    status: Optional[StatusEnum] = None

    @field_validator("title")
    def validate_title_not_null(cls, value):
        if value is None:
            raise ValueError("title cannot be null")
        return value

    @field_validator("status")
    def validate_status_not_null(cls, value):
        if value is None:
            raise ValueError("status cannot be null")
        return value

class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    status: StatusEnum
    due_date: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)
