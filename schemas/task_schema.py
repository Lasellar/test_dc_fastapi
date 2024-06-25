from pydantic import BaseModel, Field
from datetime import datetime


class TaskSchema(BaseModel):
    id: int
    title: str = Field(max_length=40)
    description: str = Field(max_length=60)
    user_id: int
    user_username: str
    period: str = Field(default=None)

    class Config:
        orm_mode = True
