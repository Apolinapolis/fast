import json
import uvicorn
from fastapi import FastAPI, HTTPException
from http import HTTPStatus
from models.User import User
from models.AppStatus import AppStatus

app = FastAPI()
users: list[User]


@app.get("/status", status_code=HTTPStatus.OK)
def status() -> AppStatus:
    return AppStatus(users=bool(users))


@app.get("/api/users/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id:int)-> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="values should be int more then one")
    if user_id > len(users):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="user not found")
    return users[user_id - 1]


@app.get("/api/users", status_code=HTTPStatus.OK)
def get_users()-> list[User]:
    return users




if __name__ == "__main__":
    with open("users.json") as f:
        users = json.load(f)

    for user in users:
        User.model_validate(user)

    print("users loaded")
    uvicorn.run(app, host='localhost', port=8002)