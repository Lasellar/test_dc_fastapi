from pydantic import BaseModel, Field
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


class TaskSchema(BaseModel):
    id: int
    title: str = Field(max_length=40)
    description: str = Field(max_length=60)
    user_id: int
    created: datetime
    deadline: datetime
    period: str = Field()
    status: str = Field()

    class Config:
        orm_mode = True
