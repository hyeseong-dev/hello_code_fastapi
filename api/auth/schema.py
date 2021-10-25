from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class UserList(BaseModel):
    id:  int = Field(None, example=1)
    email: str = Field(..., example='test@gmail.com')
    fullname: str = Field(..., example='Test')
    created_on: Optional[datetime] = None
    status: str = None


class UserCreate(BaseModel):
    email: str = Field(..., example='test@gmail.com')
    password: str = Field(..., example='test')
    fullname: str = Field(..., example='Test')


class ForgotPassword(BaseModel):
    email: str = Field(..., example='test@gmail.com')


class ResetPassword(BaseModel):
    reset_password_token: str = Field(...,
                                      example='b97b9116-341a-11ec-b960-0242ac170003')
    new_password: str = Field(..., example='testpassword')
    confirm_password: str = Field(..., example='testpassword')
