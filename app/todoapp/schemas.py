from pydantic import BaseModel
from typing import Optional

# use for validation while creating new task
class CreateTaskSchema(BaseModel):
    task: str
    # user_id: int

# use for presenting data by /get-task
class TaskListScheme(BaseModel):
    id: int
    task: str
    is_completed: bool

# use for validating email for updation
class UpdateTaskSchema(BaseModel):
    task: Optional[str] = None
    is_completed: Optional[bool] = None
