from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id:int | None = Field(default=None, primary_key=True)
    email: EmailStr
    first_name: str
    last_name: str
    avatar: str

class UserRead(SQLModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    avatar: str

    class Config:
        from_attributes = True # its really need?


class UserUpdate(SQLModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    avatar: str | None = None