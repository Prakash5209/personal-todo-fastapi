from fastapi import HTTPException,status
from app.todoapp.models import TasksModel

class TaskCreation:
    def __init__(self,schema,db,payload):
        self.schema = schema
        self.db = db
        self.payload = payload


    def create_task(self):

        # creating new task 
        new_task = TasksModel(task = self.schema.task,user_id = self.payload.get("id"))
        self.db.add(new_task)
        try:
            self.db.commit()
            self.db.refresh(new_task)
            return {"status":201,"content":"new task added"}
        except Exception as e:
            # print(e)
            self.db.rollback()
            return HTTPException(status_code = 400,detail="error while creating todo, invalid token")


class GetTask:
    def __init__(self,payload,db,skip,limit):
        self.payload = payload

        #  retrieve data according to skip and limits
        try: 
            self.taskslist = db.query(TasksModel).filter(TasksModel.user_id == self.payload.get("id")).offset(skip).limit(limit).all()
        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="tasks not found")

    def gettask(self):
        return self.taskslist




class UpdateTask:
    def __init__(self, id, schema, payload, db):
        self.id = id
        self.schema = schema
        self.payload = payload
        self.db = db

    def taskupdate(self):
        # Fetch the task belonging to the authenticated user
        that_task = self.db.query(TasksModel).filter(
            TasksModel.user_id == self.payload.get("id"),
            TasksModel.id == self.id
        ).first()

        if not that_task:
            raise HTTPException(status_code=404, detail="Task not found")

        # Partial update logic
        if self.schema.task is not None:
            that_task.task = self.schema.task

        if self.schema.is_completed is not None:
            that_task.is_completed = self.schema.is_completed # Commit changes
        try:
            self.db.commit()
            self.db.refresh(that_task)
            return that_task
        except:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Failed to update")



class DeleteTask:
    def __init__(self,id,db,payload):
        self.id = id
        self.db = db
        self.payload = payload

    def taskdelete(self):

        # First, verify task exists and belongs to the user
        task = self.db.query(TasksModel).filter(
            TasksModel.id == self.id,
            TasksModel.user_id == self.payload.get("id")
        ).first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="task not found or not authorized"
            )
        self.db.delete(task) #  state delete
        self.db.commit() # delete operation performed
        return {"status": 200, "message": "Task deleted successfully"}
