import jwt

from jwt import PyJWTError
from pydantic import ValidationError

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from datetime import datetime, timedelta
from api.utils import const_util
from api.auth import crud, schema



async def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minute=15)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, const_util.SECRET_KEY, algorithm=const_util.ALGORITHM_HS256)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/api/v1/auth/login'
)

def get_token_user(token: str = Depends(oauth2_scheme)):
    return token


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={'WWW-Authenticate':'Bearer'}
    )

    try:
        payload = jwt.decode(token, const_util.SECRET_KEY, algorithms=[const_util.ALGORITHM_HS256] )
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        
        # Check blacklist token
        black_list_token = await crud.find_black_list_token(token)
        if black_list_token:
            raise credentials_exception

        # Check user existed
        result = await crud.find_user_exist(username)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User NOT FOUND")
        
        return schema.UserList(**result)

    except(PyJWTError, ValidationError):
        raise credentials_exception

def get_current_active_user(current_user: schema.UserList = Depends(get_current_user)):
    if current_user.status != '1':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Inactive User')
    return current_user