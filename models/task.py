from sqlalchemy import (
    Column, Integer, String, ForeignKey,
    DateTime, func
)
from sqlalchemy.orm import relationship
import datetime as dt

from database import Base


class TaskModel(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    description = Column(String, index=True)
    user = relationship('UserModel', back_populates='tasks')
    user_id = Column(Integer, ForeignKey('users.id'))
    """created = Column(DateTime, default=dt.datetime.now().date(), index=True)
    deadline = Column(
        DateTime,
        default=created+dt.timedelta(days=7), index=True)
    period = Column(String, index=True)

    @property
    def period(self):
        return f'{str(self.created)}-{str(self.deadline)}'"""
