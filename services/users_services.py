from sqlalchemy.orm import Session

from models.user import UserModel
from dto import user_dto


def create_user(data: user_dto.User, db: Session):
    user = UserModel(**data.dict())
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as ex:
        print(ex)
        return ex
    return user


def get_user(id: int, db: Session):
    user = db.query(UserModel).filter(UserModel.id == id).first()
    if user:
        return user
    return 'User does not exist'


def update(id: int, data: user_dto.User, db: Session):
    user = db.query(UserModel).filter(UserModel.id == id).first()
    user.username = data.username
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def remove(id: int, db: Session):
    user = db.query(UserModel).filter(UserModel.id == id).first()
    db.commit()
    return user
