from sqlalchemy import (
    Column, Integer, String, Boolean
)
from sqlalchemy.orm import relationship

from database import Base


class UserModel(Base):
    __tablename__ = 'users'
    # посмотреть mapped column

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    tasks = relationship('TaskModel', back_populates='user')
