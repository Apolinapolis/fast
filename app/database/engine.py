import os
from sqlalchemy.orm import Session
from sqlmodel import SQLModel, create_engine, text



engine = create_engine(os.getenv("DATABASE_ENGINE"), pool_size=int (os.getenv("POOL_SIZE", 10)))


def create_db_tables():
    SQLModel.metadata.create_all(engine)


def check_db_available() -> bool:
    try:
        with Session(engine) as s:
            s.execute(text('SELECT 1'))
            return True
    except Exception as e:
        print(e)
        return False
