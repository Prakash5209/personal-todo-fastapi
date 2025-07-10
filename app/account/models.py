from __future__ import annotations
from sqlalchemy import DateTime, String
from sqlalchemy.orm import mapped_column,Mapped,relationship
import datetime
from typing import TYPE_CHECKING,List


from database import Base # -> DeclarativeBase()
from app.notes.models import TasksModel
   

class TimeStamp:
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),default=datetime.datetime.now(datetime.timezone.utc)
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),default=datetime.datetime.now(datetime.timezone.utc),
        onupdate=datetime.datetime.now(datetime.timezone.utc)
    )


class UserModel(Base,TimeStamp): # inheritating TimeStamp - auto manages Timestamp
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(primary_key=True)

    # nullable = False, doesn't allow fields to be empty
    full_name: Mapped[str] = mapped_column(String(50),nullable=False)
    email: Mapped[str] = mapped_column(String(100),nullable=False,unique=True) # email formatting will be done in account.routers 
    password: Mapped[str] = mapped_column(String(100),nullable=False)

    tasksmodel: Mapped[List["TasksModel"]] = relationship(
        "TasksModel",
        back_populates="usermodel"
    ) # one (User) to many (task) relationship

 
