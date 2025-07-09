from sqlalchemy.orm import sessionmaker,Session,DeclarativeBase
from sqlalchemy import create_engine
from fastapi import Depends

from typing import Annotated

engine = create_engine("postgresql+psycopg2://postgres@localhost:5432/todo",echo=True)

SessionLocal = sessionmaker(autoflush=False,bind=engine,autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session,Depends(get_db)]



class Base(DeclarativeBase):
    pass
