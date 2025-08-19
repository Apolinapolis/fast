from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy import select
from sqlmodel import Session
from app.models.User import User, UserUpdate
from .engine import engine


def get_user(user_id) -> User|None:
    with Session(engine) as session:
        return session.get(User, user_id)


def get_users() -> list[User]:
    with Session(engine) as s:
        statement = select(User)
        return s.exec(statement).scalars().all()



def create_user(user: User) -> User:
    with Session(engine) as s:
        s.add(user)
        s.commit()
        s.refresh(user)
        return user


def update_user(user_id:int, payload:UserUpdate):
    with Session(engine) as s:
        db_user = s.get(User, user_id)
        if not db_user:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail= 'user not found') #layer refactoring is needed
        user_data = payload.model_dump(exclude_unset=True)
        db_user.sqlmodel_update(user_data)
        s.add(db_user)
        s.commit()
        s.refresh(db_user)
        return db_user


def delete_user(user_id:int):
    with Session(engine) as s:
        user = s.get(User, user_id)
        s.delete(user)
        s.commit()