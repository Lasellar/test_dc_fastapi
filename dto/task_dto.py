from pydantic import BaseModel


class Task(BaseModel):
    title: str
    description: str
    user_id: int
