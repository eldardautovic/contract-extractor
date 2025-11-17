from typing import Annotated
from fastapi import Depends
from core.config import settings
from sqlmodel import SQLModel, Session, create_engine

#importing models so engine SQLModel knows to map them
from . import models

engine = create_engine(
    settings.DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False} 
)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)