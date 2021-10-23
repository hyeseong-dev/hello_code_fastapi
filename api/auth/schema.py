from pydantic import BaseModel, Field


class UserList(BaseModel):
    email: str = Field(..., example='test@gmail.com')
    fullname: str = Field(..., example='Test')


class UserCreate(BaseModel):
    email: str = Field(..., example='test@gmail.com')
    password: str = Field(..., example='test')
    fullname: str = Field(..., example='Test')


class UserPassword(BaseModel):
    password: str
