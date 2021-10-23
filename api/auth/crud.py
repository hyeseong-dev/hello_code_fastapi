from api.utils.db_util import database
from api.auth import schema


def find_user_exist(email: str):
    query = "select * from py_users where email=:email and status='1'"
    return database.fetch_one(query, values={'email': email})


def save_user(user: schema.UserCreate):
    query = "INSERT INTO py_users VALUES (nextval('user_id_seq'), :email, :password, :fullname, now() at time zone 'Asia/Seoul', '1')"
    return database.execute(query, values={'email': user.email, 'password': user.password, 'fullname': user.fullname})
