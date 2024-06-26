import jwt
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from auth.models import UserAuthModel
from database import Base

SECRET_KEY = 'f684589d8093a71d784a3f39abbc0e5873352b3af5fa15033586b55e3fdaa9edaff3870d66cbda82ddd422a649f249463cec2a3fde7985d872ae5f02513e987b'
REFRESH_KEY = '7dbf35a3d20aeb8d5e3fedbb159224883d9f360895688f9698daf3f903513bea9643fbb25a75164b384eb062c83a8a0e702a517849ed2a38a432e7c9c0fea35e'
ALGORITHM = 'HS256'
EXPIRATION_TIME_ACCESS_TOKEN = timedelta(minutes=10)
EXPIRATION_TIME_REFRESH_TOKEN = timedelta(days=7)


def refresh_token(refresh_token: str, db: Session):
    try:
        decoded_data = jwt.decode(
            refresh_token, REFRESH_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid refresh token'
        )
    user = db.query(UserAuthModel).filter(
        UserAuthModel.username == decoded_data['sub']).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user not found'
        )
    new_access_token = create_access_token({'sub': user.username})
    new_refresh_token = create_refresh_token({'sub': user.username})
    return {
        'access_token': new_access_token,
        'refresh_token': new_refresh_token
    }


def create_refresh_token(data: dict):
    """Создает рефреш токен"""
    expiration = datetime.utcnow() + EXPIRATION_TIME_ACCESS_TOKEN
    data.update({'exp': expiration})
    encoded_jwt = jwt.encode(data, REFRESH_KEY, algorithm=ALGORITHM)
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


def update_tokens():
    pass
