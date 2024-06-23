from pydantic import BaseModel
from typing import List

from dto.task_dto import Task


class User(BaseModel):
    username: str
    tasks: List[Task]
