from sqlalchemy.orm import Session

from models.task import TaskModel
from dto import task_dto


def get_task_queryset(identifier: int | str, db: Session):
    queryset = db.query(TaskModel).filter(
        TaskModel.id == identifier).first()
    if not queryset:
        queryset = db.query(TaskModel).filter(
            TaskModel.title == identifier).first()
    if queryset:
        return queryset
    return 'ERROR: Task not found'


def create_task(data: task_dto.Task, db: Session):
    task = TaskModel(**data.dict())
    try:
        with db:
            db.add(task)
            db.commit()
            db.refresh(task)
    except Exception as ex:
        return ex
    return task


def get_task(identifier: int | str, db: Session):
    return get_task_queryset(identifier, db)


def get_tasks(db: Session):
    return db.query(TaskModel).all()


def update_task(
        identifier: int | str,
        data: task_dto.TaskUpdate,
        db: Session
):
    task = get_task_queryset(identifier, db)

    task.title = data.title if data.title else task.title
    task.description = data.description if data.description else task.description
    task.deadline = data.deadline if data.deadline else task.deadline
    task.status = data.status if data.status else task.status

    try:
        with db:
            db.add(task)
            db.commit()
            db.refresh(task)
    except Exception as ex:
        return ex
    return task


def delete_task(
    identifier: int | str,
    db: Session
):
    task = get_task_queryset(identifier, db)
    try:
        with db:
            db.delete(task)
            db.commit()
    except Exception as ex:
        print(ex)
        return ex
    return task

