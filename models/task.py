from sqlalchemy import (
    Column, Integer, String,
    DateTime
)
import datetime as dt
from pytz import timezone

from database import Base


class TaskModel(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    description = Column(String)
    created = Column(
        DateTime,
        default=dt.datetime.now(timezone('UTC')).date,
    )
    deadline = Column(
        DateTime,
        default=(
            dt.datetime.now(timezone('UTC')) + dt.timedelta(days=7)
        ).date
    )
    period = Column(String)
    status = Column(String, default='not started')

    @property
    def period(self):
        return (f"{str(self.created.strftime('%d.%m.%y'))}"
                f"-{str(self.deadline.strftime('%d.%m.%y'))}")
