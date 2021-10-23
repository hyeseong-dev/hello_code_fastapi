from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

import jwt

from api.auth import schema
from api.auth import crud
from api.utils import crypto_util, jwt_util, const_util


router = APIRouter(
    prefix='/api/v1'
)


@router.post('/auth/register', response_model=schema.UserList)
async def register(payload: schema.UserCreate):
    # Check User Exist
    result = await crud.find_user_exist(payload.email)
    if result:
        raise HTTPException(status_code=404, detail='User already registered.')

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
            status_code=403, detail='Incorrect username or password')

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
