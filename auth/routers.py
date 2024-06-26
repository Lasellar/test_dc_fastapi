import jwt
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session, Mapped

from auth.dto import User4Auth, UserResponse
from auth.funcs4auth import (
    create_access_token, create_refresh_token,
    verify_token,
)
from auth.funcs4auth import refresh_token as refresh
from auth.models import UserAuthModel
from database import get_db


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    decoded_data = verify_token(token)
    if not decoded_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='invalid token')
    user = db.query(UserAuthModel).filter(
        UserAuthModel.username == decoded_data['sub']).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='user not found')
    return user


@router.post(
    '/register',
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse
)
def register_user(
        data: User4Auth,
        db: Session = Depends(get_db)
):
    """
    Регистрирует юзера.
    Возвращает username, hashed_password, disabled
    """
    hashed_password = pwd_context.hash(data.password)
    data.hashed_password = hashed_password
    user = UserAuthModel(**data.dict())
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as ex:
        return ex
    return user


@router.post(
    '/token',
    status_code=status.HTTP_200_OK,
)
def authenticate_user(data: User4Auth, db: Session = Depends(get_db)):
    user = db.query(UserAuthModel).filter(
        UserAuthModel.username == data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='incorrect username or password'
        )
    is_password_correct = pwd_context.verify(
        data.password, user.hashed_password)
    if not is_password_correct:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='incorrect username or password'
        )
    jwt_token = create_access_token({'sub': user.username})
    refresh_token_ = create_refresh_token({'sub': data.init_data})
    return {'access_token': jwt_token, 'refresh_token': refresh_token_}


@router.get('/users/me')
def get_user_me(current_user: UserAuthModel = Depends(get_current_user)):
    return current_user


@router.post('/refresh_token')
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    return refresh(refresh_token, db)

