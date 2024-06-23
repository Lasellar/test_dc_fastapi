from sqlalchemy.orm import Session

from models.task import TaskModel
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
    if type(identifier) == int:
        return db.query(TaskModel).filter(
            TaskModel.id == identifier).first()
    return db.query(TaskModel).filter(
        TaskModel.title == identifier).first()


def get_tasks(db: Session):
    return db.query(TaskModel).all()

