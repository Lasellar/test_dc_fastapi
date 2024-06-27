from aiogram.utils.web_app import WebAppInitData, WebAppUser, WebAppChat
from sqlalchemy import Integer, String, Boolean, ForeignKey, Column, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime

from database import Base


class UserAuthModel(Base):
    __tablename__ = 'usersauth'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    raw_init_data: Mapped[str] = mapped_column(String, nullable=False)
    init_data: Mapped[WebAppInitData] = mapped_column(nullable=True)

    username: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    tg_id: Mapped[int] = mapped_column(Integer, nullable=True)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    is_premium: Mapped[bool] = mapped_column(Boolean, nullable=True)
    photo_url: Mapped[str] = mapped_column(String, nullable=True)
    language_code: Mapped[str] = mapped_column(String, nullable=True)

    tg_query_id: Mapped[str] = mapped_column(String, nullable=True)
    tg_user: Mapped[WebAppUser] = mapped_column(nullable=True)
    tg_reciever: Mapped[WebAppUser] = mapped_column(nullable=True)
    tg_chat: Mapped[WebAppChat] = mapped_column(nullable=True)
    tg_chat_type: Mapped[str] = mapped_column(String, nullable=True)
    tg_chat_instance: Mapped[str] = mapped_column(String, nullable=True)
    tg_start_param: Mapped[str] = mapped_column(String, nullable=True)
    tg_can_send_after: Mapped[int] = mapped_column(Integer, nullable=True)
    tg_auth_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    tg_hash: Mapped[str] = mapped_column(String, nullable=True)


