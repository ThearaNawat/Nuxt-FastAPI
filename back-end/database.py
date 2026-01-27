from sqlmodel import SQLModel, create_engine, Session
from config import settings
from typing import Annotated
from fastapi import Depends
import model
DATABASE_URL = 'postgresql://postgres:123456@localhost:5433/inventory'
# DATABASE_URL = 'postgresql://postgres:123456@host.docker.internal:5433/inventory'

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_table():
    SQLModel.metadata.create_all(engine)
    

def get_session():
    with Session(engine) as session:
        yield session
        
SessionDep = Annotated[Session, Depends(get_session)]