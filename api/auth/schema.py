from pydantic import BaseModel, Field


class UserList(BaseModel):
    email: str = Field(..., example='test@gmail.com')
    fullname: str = Field(..., example='Test')


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
