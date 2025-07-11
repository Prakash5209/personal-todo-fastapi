from __future__ import annotations
from sqlalchemy import DateTime, String
from sqlalchemy.orm import mapped_column,Mapped,relationship
import datetime
from typing import List


from database import Base # -> DeclarativeBase()
from app.todoapp.models import TasksModel
   


# abstract (mixin) class
class TimeStamp:
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
        onupdate=lambda: datetime.datetime.now(datetime.timezone.utc)
    )


class UserModel(Base,TimeStamp): # inheritating TimeStamp - auto manages Timestamp
    __tablename__ = "user_table" # table name in the database

    id: Mapped[int] = mapped_column(primary_key=True) # primary_key + autoincreament by default

    # nullable = False, doesn't allow fields to be empty
    full_name: Mapped[str] = mapped_column(String(50),nullable=False)
    email: Mapped[str] = mapped_column(String(100),nullable=False,unique=True) # email formatting will be done in account.services.account_services.py
    password: Mapped[str] = mapped_column(String(100),nullable=False) # store hash password (bcrypt)

    tasksmodel: Mapped[List["TasksModel"]] = relationship(
        "TasksModel",
        back_populates="usermodel",
        cascade="all, delete-orphan"
    ) # one (User) to many (task) relationship

 
