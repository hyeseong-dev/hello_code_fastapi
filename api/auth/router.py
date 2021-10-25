import jwt
import uuid

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from api.auth import schema
from api.auth import crud
from api.utils import crypto_util, jwt_util, const_util, email_util

from api.exceptions.business import BusinessException

router = APIRouter(
    prefix='/api/v1'
)


@router.post('/auth/register', response_model=schema.UserList)
async def register(payload: schema.UserCreate):
    # Check User Exist
    result = await crud.find_user_exist(payload.email)
    if result:
        # raise HTTPException(status_code=404, detail='User Already Registered.')
        raise BusinessException(status_code=409, detail="User Already Registerd")
    # Create New User
    # hash password here
    payload.password = crypto_util.hash_password(payload.password)
    await crud.save_user(payload)
    return {**payload.dict()}


@router.post('/auth/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Check user existed
    result = await crud.find_user_exist(form_data.username)
    if not result:
        raise HTTPException(status_code=404, detail='User Not Found')

    # Verify Password
    user = schema.UserCreate(**result)
    verified_password = crypto_util.verify_password(
        form_data.password, user.password)

    if not verified_password:
        raise HTTPException(
            status_code=403, detail='Incorrect Username Or password')

    # Create Token
    access_token_expires = jwt_util.timedelta(
        minutes=const_util.ACCESS_TOKEN_EXPIRE_MINUTE)
    access_token = await jwt_util.create_access_token(
        data={'sub': form_data.username},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": 'Bearer',
        "user_info": {
            "email": user.email,
            "fullname": user.fullname
        }
    }


@router.post('/auth/forgot_password')
async def forgot_password(request: schema.ForgotPassword):
    # Check user existed
    result = await crud.find_user_exist(request.email)
    if not result:
        raise HTTPException(status_code=404, detail='User Not Found')

    # Create reset code and save in database
    reset_code = str(uuid.uuid1())
    await crud.create_reset_code(request.email, reset_code)

    # Sending Email
    subject = 'Hello Coder'
    recipient = [request.email]
    message = f"""
    <!DOCTYPE html>
    <html>
    <title> Reset Password</title>
    <body>
    <div style="width:100%; font-family: monospace;">
        <h1>Hello, {request.email}</h1>
        <p>Someone has requested a link to reset your password. If you requested this, you can change your password through th button below.</p>
        <a href="http://127.0.0.1:8000/user/forgot-password?reset_password_token={reset_code}"></a>
        <p>If you didn't request this, you can ignore this email.</p>
        <p>Your password won't change until you access the link above and create a new one.</p>
    </div>
    </body>
    </html>
    """

    await email_util.send_email(subject, recipient, message)

    return {
        "reset_code": reset_code,
        "code": 200,
        "message": "We've Sent An Email With Instaruction To Reset Your Password"
    }


@router.patch('/auth/reset-password')
async def reset_password(request: schema.ResetPassword):
    # Check valid reset password token
    reset_token = await crud.check_reset_password_token(request.reset_password_token)
    if not reset_token:
        raise HTTPException(
            status_code=404, detail="Reset Password Token Has Expired, Please Request A New One.")

    # Check Both new & confirm password are matched
    if request.new_password != request.confirm_password:
        raise HTTPException(status_code=400, detail="Password Not Match")

    # Reset New Password
    forgot_password_object = schema.ForgotPassword(**reset_token)
    new_hashed_password = crypto_util.hash_password(request.new_password)
    await crud.reset_password(new_hashed_password, forgot_password_object.email)

    # Disable reset code (already used)
    await crud.disable_reset_code(request.reset_password_token, forgot_password_object.email)

    return {
        "code": 200,
        "message": "Password Has Been Reset Successfully"
    }
