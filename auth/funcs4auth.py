import jwt
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from auth.models import UserAuthModel
from database import Base

SECRET_KEY = 'f684589d8093a71d784a3f39abbc0e5873352b3af5fa15033586b55e3fdaa9edaff3870d66cbda82ddd422a649f249463cec2a3fde7985d872ae5f02513e987b'
ALGORITHM = 'HS256'
EXPIRATION_TIME_ACCESS_TOKEN = timedelta(minutes=10)
EXPIRATION_TIME_REFRESH_TOKEN = timedelta(days=7)


def refresh_token(refresh_token: str, db: Session):
    try:
        decoded_data = jwt.decode(
            refresh_token, refresh_token, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid refresh token'
        )
    user = db.query(UserAuthModel).filter(
        UserAuthModel.init_data == decoded_data['sub']).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user not found'
        )
    new_access_token = create_access_token({'sub': user.username})
    new_refresh_token = create_refresh_token({'sub': user.init_data})
    return {
        'access_token': new_access_token,
        'refresh_token': new_refresh_token
    }


def create_refresh_token(data: dict):
    """Создает рефреш токен"""
    expiration = datetime.utcnow() + EXPIRATION_TIME_ACCESS_TOKEN
    data.update({'exp': expiration})
    encoded_jwt = jwt.encode(data, data['sub'], algorithm=ALGORITHM)
    return encoded_jwt


def create_access_token(data: dict):
    """Создает JWT токен."""
    expiration = datetime.utcnow() + EXPIRATION_TIME_ACCESS_TOKEN
    data.update({'exp': expiration})
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token: str):
    """Верификация токена."""
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_data
    except jwt.PyJWTError:
        return None
