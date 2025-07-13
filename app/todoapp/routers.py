from fastapi import APIRouter,Depends

from database import db_dependency
from app.todoapp.schemas import CreateTaskSchema, TaskListScheme
from app.todoapp.services.todo_service import DeleteTask, TaskCreation,GetTask, UpdateTask
from app.tokenparser import parse_token
from app.todoapp.schemas import UpdateTaskSchema

from typing import List


router = APIRouter()

# creating new task, token is needed
@router.post("/new-task")
def new_task(schema: CreateTaskSchema,db: db_dependency,payload: dict = Depends(parse_token)):

    # app.todoapp.services todo_service.py file
    task_obj = TaskCreation(schema = schema,db = db,payload=payload)
    val = task_obj.create_task()
    return val


# retrieve task with query parameter
@router.get("/get-task",response_model=List[TaskListScheme]) # response_model to show valid information only
def get_task(skip: int,limit: int ,db: db_dependency, payload: dict = Depends(parse_token)):
    gettask_obj = GetTask(payload = payload,db = db,skip=skip,limit=limit)
    task_list = gettask_obj.gettask()
    return task_list


# remove task with task id and user's task 
@router.delete("/delete-task/{id}")
def delete_task(id: int, db: db_dependency, payload: dict = Depends(parse_token)):
    deletetask_obj = DeleteTask(id = id,db = db, payload = payload)
    result = deletetask_obj.taskdelete()
    return result


# update todo instance with id
@router.patch("/update-task/{id}")
def update_task(id: int, schema: UpdateTaskSchema, db: db_dependency, payload: dict = Depends(parse_token)):
    updatetask_obj = UpdateTask(id = id, schema = schema, payload = payload, db = db)
    result = updatetask_obj.taskupdate()
    return result

