from pydantic import BaseModel, Field
from datetime import datetime


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
