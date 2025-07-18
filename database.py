from sqlalchemy.orm import sessionmaker,Session,DeclarativeBase
from sqlalchemy import create_engine
from fastapi import Depends

from typing import Annotated

engine = create_engine("postgresql+psycopg2://postgres@localhost:5432/crawlertask",echo=True)


# binding engine to session for clean database connnection
SessionLocal = sessionmaker(autoflush=False,bind=engine,autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session,Depends(get_db)]


# Base class to create database from 
class Base(DeclarativeBase):
    pass
