from pydantic import BaseModel, Field
from datetime import datetime


class TaskSchema(BaseModel):
    id: int
    title: str = Field(max_length=40)
    description: str = Field(max_length=60)
    user_id: int
    period: str = Field(default=None)
    status: str = Field(max_length=15)

    class Config:
        orm_mode = True
