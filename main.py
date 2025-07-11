from fastapi import FastAPI

from app.account.routers import router as account_router
from app.todoapp.routers import router as todoapp_router

# initializing fastapi to app 
app = FastAPI()


app.include_router(account_router) # app/account base router connection
app.include_router(todoapp_router) # app/todoapp router connection



