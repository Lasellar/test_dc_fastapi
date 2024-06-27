import jwt
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from aiogram.utils.web_app import (
    check_webapp_signature, parse_webapp_init_data, WebAppInitData
)


from auth.models import UserAuthModel
from database import Base

SECRET_KEY = 'f684589d8093a71d784a3f39abbc0e5873352b3af5fa15033586b55e3fdaa9edaff3870d66cbda82ddd422a649f249463cec2a3fde7985d872ae5f02513e987b'
ALGORITHM = 'HS256'
EXPIRATION_TIME_ACCESS_TOKEN = timedelta(minutes=10)
BOT_TOKEN = '12345qwerty'


class InitDataValidationError(Exception):
    def __init__(self):
        self.message = 'invalid init data string received'
        super().__init__(self.message)


def get_init_data(raw_init_data: str, token: str = BOT_TOKEN):
    is_init_data: bool = check_webapp_signature(token, raw_init_data)
    if is_init_data:
        init_data: WebAppInitData = parse_webapp_init_data(
            init_data=raw_init_data
        )
        return {'raw_init_data': raw_init_data, 'init_data': init_data}
    raise InitDataValidationError


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
    return {
        'access_token': new_access_token,
        'refresh_token': get_init_data()
    }


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
