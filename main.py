from fastapi import FastAPI

from app.account.routers import router as account_router

app = FastAPI()


app.include_router(account_router)


