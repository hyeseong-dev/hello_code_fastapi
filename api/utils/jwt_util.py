import jwt

from datetime import datetime, timedelta
from api.utils import const_util


async def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minute=15)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, const_util.SECRET_KEY, algorithm=const_util.ALGORITHM_HS256)
