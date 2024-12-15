from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    password: str


class UserRead(UserBase):
    pass


class UserWrite(UserBase):
    id: int