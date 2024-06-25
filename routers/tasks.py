from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from services import tasks_services as ts
from dto import task_dto
from schemas.task_schema import TaskSchema


router = APIRouter()


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=TaskSchema,
    responses={
        404: {'description': 'Not found'}
    }
)
def create(data: task_dto.Task, db: Session = Depends(get_db)):
    return ts.create_task(data=data, db=db)


@router.get(
    '/get_all',
    status_code=status.HTTP_200_OK
)
def get_tasks(db: Session = Depends(get_db)):
    return ts.get_tasks(db=db)


@router.get(
    '/{identifier}',
    status_code=status.HTTP_200_OK
)
def get_task(identifier: int | str, db: Session = Depends(get_db)):
    return ts.get_task(identifier=identifier, db=db)


@router.patch(
    '/{identifier}',
    status_code=status.HTTP_201_CREATED,
    response_model=TaskSchema
)
def update(
    identifier: int | str,
    data: task_dto.TaskUpdate,
    db: Session = Depends(get_db),
):
    return ts.update_task(
        identifier=identifier,
        data=data,
        db=db
    )


@router.delete(
    '/{identifier}',
    status_code=200,
    response_model=TaskSchema
)
def delete(
    identifier: int | str,
    db: Session = Depends(get_db)
):
    return ts.delete_task(identifier=identifier, db=db)
