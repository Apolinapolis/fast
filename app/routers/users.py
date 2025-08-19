from fastapi import FastAPI, HTTPException, APIRouter
from typing import Iterable
from http import HTTPStatus
from app.models.User import User, UserUpdate, UserRead
from app.database import users



app = FastAPI()
router = APIRouter(prefix='/api/users')


@router.get("/{user_id}", response_model=User, status_code=HTTPStatus.OK)
def get_user(user_id:int)-> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="values should be int more then one")
    user = users.get_user(user_id)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="user not found")
    return user


@router.get("", response_model=list[UserRead], status_code=HTTPStatus.OK)
def get_users()-> Iterable[User]:
    return users.get_users()


@router.post("", status_code=HTTPStatus.CREATED)
def create_user(user: User) -> User:
    User.model_validate(user.model_dump())
    return users.create_user(user)


@router.patch("/{user_id}", status_code=HTTPStatus.OK)
def update_user(user_id:int, user: UserUpdate) -> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="values should be int more then one")
    UserUpdate.model_validate(user.model_dump())
    return users.update_user(user_id,user)


@router.delete("/{user_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_user(user_id:int):
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY,detail="values should be int more then one")
    users.delete_user(user_id)
    return {'message':'user deleted'}