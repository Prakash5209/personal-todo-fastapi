from sqlalchemy import Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import mapped_column,Mapped, relationship
import datetime
from typing import TYPE_CHECKING


from database import Base

# To avoid python circular import issue
if TYPE_CHECKING:
    from app.account.models import UserModel


# Abstract (Mixin) class
class TimeStamp:
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),default = lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default = lambda: datetime.datetime.now(datetime.timezone.utc),
        onupdate = lambda: datetime.datetime.now(datetime.timezone.utc)
    )


class TasksModel(Base,TimeStamp): # inheritating TimeStamp - auto manages Timestamp
    __tablename__ = "task_model"

    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[str] = mapped_column(Text)
    is_completed: Mapped[bool] = mapped_column(Boolean,default=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    usermodel: Mapped["UserModel"] = relationship(back_populates="tasksmodel") # access UserModel data from TasksModel with 'tasks'

