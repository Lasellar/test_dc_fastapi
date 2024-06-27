import jwt
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session, Mapped

from auth.dto import User4Auth, UserResponse
from auth.funcs4auth import (
    create_access_token,
    verify_token, get_init_data,
)
from auth.funcs4auth import refresh_token as refresh
from auth.models import UserAuthModel
from database import get_db


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
RAW_INIT_DATA = ('user=%7B%22'
                 'id%22%3A240399316%2C%22'
                 'first_name%22%3A%22spoonfulofdust%22%2C%22'
                 'last_name%22%3A%22%22%2C%22'
                 'username%22%3A%22r_u_dust%22%2C%22'
                 'language_code%22%3A%22en%22%2C%22'
                 'is_premium%22%3Atrue%2C%22'
                 'allows_write_to_pm%22%3Atrue%7D&'
                 'chat_instance=9053424214772612934&'
                 'chat_type=private&'
                 'auth_date=1719435839&'
                 'hash=746919017ac0db4a955125e7f01cc6f7322eafadd971a57ba946850a532b82f6')


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
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse
)
def register_user(
        data: User4Auth,
        db: Session = Depends(get_db)
):
    """
    Регистрирует юзера и возвращает его токен
    """
    user = UserAuthModel(**data.dict())
    jwt_token = create_access_token({'sub': user.username})
    refresh_token = data.init_data
    init_data = get_init_data(
        raw_init_data=data['raw_init_data'])['init_data']
    init_data_user = init_data.user

    user.username = init_data_user.username
    user.tg_id = init_data_user.id
    user.first_name = init_data_user.first_name
    user.last_name = init_data_user.last_name
    user.is_premium = init_data_user.is_premium
    user.photo_url = init_data_user.photo_url
    user.language_code = init_data_user.language_code

    user.query_id = init_data.query_id
    user.tg_user = init_data_user
    user.tg_reciever = init_data.reciever
    user.tg_chat = init_data.chat
    user.tg_chat_type = init_data.chat_type
    user.tg_chat_instance = init_data.chat_instance
    user.tg_start_param = init_data.start_param
    user.tg_can_send_after = init_data.can_send_after
    user.tg_auth_date = init_data.auth_date
    user.tg_hash = init_data.hash

    try:
        with db:
            db.add(user)
            db.commit()
            db.refresh(user)
    except Exception as ex:
        return ex
    return {
        'username': user.username,
        'access_token': jwt_token,
        'refresh_token': refresh_token
    }


@router.get('/users/me')
def get_user_me(current_user: UserAuthModel = Depends(get_current_user)):
    return current_user


@router.post('/refresh_token')
def refresh_token(data: dict, db: Session = Depends(get_db)):
    refresh_token_ = data['raw_init_data']
    return refresh(refresh_token_, db)

