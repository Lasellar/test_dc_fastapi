from sqlalchemy.orm import Session

from models.task import TaskModel
from schemas.task_schema import TaskSchema
from models.user import UserModel
from dto import task_dto


def create_task(data: task_dto.Task, db: Session):
    task = TaskModel(**data.dict())
    try:
        db.add(task)
        db.commit()
        db.refresh(task)
    except Exception as ex:
        print(ex)
        return ex
    return task


def get_task(identifier: int | str, db: Session):
    queryset = db.query(TaskModel).filter(
        TaskModel.id == identifier).first()
    if not queryset:
        queryset = db.query(TaskModel).filter(
            TaskModel.title == identifier).first()
    if queryset:
        return queryset
    return '11111111'


def get_tasks(db: Session):
    return db.query(TaskModel).all()

