from sqlalchemy import DateTime, String
from sqlalchemy.orm import mapped_column,Mapped,relationship
import datetime
from typing import TYPE_CHECKING,List


from database import Base # -> DeclarativeBase()


# to prevent circular import issues at runtime.
if TYPE_CHECKING:
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

    # nullalble = False, doesn't allow fields to be empty
    full_name: Mapped[str] = mapped_column(String(255),nullable=False)
    email: Mapped[str] = mapped_column(String(255),nullable=False) # email formatting will be done in account.routers 
    password: Mapped[str] = mapped_column(String(255),nullable=False)

    tasks: Mapped[List["TasksModel"]] = relationship(back_populates="usermodel") # one (User) to many (task) relationship

    
