from fastapi import APIRouter, Depends, HTTPException
from api.auth import schema
from api.auth import crud
from api.utils import crypto_util

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
