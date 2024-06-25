from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Task(BaseModel):
    title: str
    description: str
    user_id: int


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    deadline: datetime | None = None
    status: str | None = None
