from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from services import tasks_services as ts
from dto import task_dto


router = APIRouter()


@router.post('/', tags=['task'])
def create(data: task_dto.Task, db: Session = Depends(get_db)):
    return ts.create_task(data=data, db=db)


@router.get('/get_all', tags=['task'])
def get_tasks(db: Session = Depends(get_db)):
    return ts.get_tasks(db=db)


@router.get('/{identifier}', tags=['task'])
def get_task(identifier: int | str = None, db: Session = Depends(get_db)):
    return ts.get_task(identifier=identifier, db=db)
