from sqlalchemy.orm import Session

from models.user import UserModel
from dto import user_dto


async def create_user(data: user_dto.User, db: Session):
    user = UserModel(**data.dict())
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as ex:
        print(ex)
        return ex
    return user


async def get_user(id: int, db: Session):
    return db.query(UserModel).filter(UserModel.id == id).first()


async def update(id: int, data: user_dto.User, db: Session):
    user = db.query(UserModel).filter(UserModel.id == id).first()
    user.username = data.username
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def remove(id: int, db: Session):
    user = db.query(UserModel).filter(UserModel.id == id).first()
    db.commit()
    return user
