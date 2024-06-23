from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from services import users_services
from dto import user_dto


router = APIRouter()


@router.post('/', tags=['user'])
def create(data: user_dto.User = None, db: Session = Depends(get_db)):
    return users_services.create_user(data=data, db=db)


@router.get('/{id}', tags=['user'])
def get(id: int = None, db: Session = Depends(get_db)):
    return users_services.get_user(id=id, db=db)


@router.put('/{id}', tags=['user'])
def update(id: int = None, data: user_dto.User = None, db: Session = Depends(get_db)):
    return users_services.update(data=data, db=db, id=id)


@router.delete('/{id}', tags=['user'])
def delete(id: int = None, db: Session = Depends(get_db)):
    return users_services.remove(db=db, id=id)
