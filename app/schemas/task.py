from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from datetime import datetime, timezone, timedelta
INDIA_TZ = timezone(timedelta(hours=5, minutes=30))

def validate_due_date(value):
    if value is None:
        return None

    if value.tzinfo is not None:
        due_date = value.astimezone(INDIA_TZ).date()
    else:
        due_date = value.date()

    today = datetime.now(INDIA_TZ).date()

    if due_date < today:
        raise ValueError("Due date cannot be in the past")

    return value

# CREATE TASK SCHEMA
class TaskCreate(BaseModel):

    title: str = Field(
        min_length=3,
        max_length=100
    )

    description: Optional[str] = None
    status: Literal[ "pending", "in_progress", "completed" ] = "pending"
    priority: Literal[ "low", "medium","high"] = "medium"
    due_date: Optional[datetime] = None

    @field_validator("due_date")
    @classmethod
    def check_due_date(cls, value):
        return validate_due_date(value)

# UPDATE TASK SCHEMA
class TaskUpdate(BaseModel):

    title: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    description: Optional[str] = None
    status: Optional[
        Literal["in_progress", "completed"]
    ] = None
    priority: Optional[
        Literal["low", "medium", "high"]
    ] = None
    due_date: Optional[datetime] = None

    @field_validator("due_date")
    @classmethod
    def check_due_date(cls, value):
        return validate_due_date(value)

# TASK RESPONSE SCHEMA
class TaskResponse(BaseModel):

    id: int
    title: str
    description: Optional[str] = None
    status: str
    priority: str
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }
