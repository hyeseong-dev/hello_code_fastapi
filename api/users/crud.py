from api.users import schema as user_schema, crud as auth_crud
from api.auth import schema as auth_schema, crud as user_crud
from api.utils.db_util import database
from api.otp import crud

def update_user(
    request: user_schema.UserUpdate,
    current_user: auth_schema.UserList
):
    
    query = 'UPDATE py_users SET fullname=:fullname where email=:email'
    return database.execute(query, values={'fullname':request.fullname, 'email': current_user.email})


def deactivate_user(
    current_user: auth_schema.UserList
):
    query = "UPDATE py_users SET status='9' WHERE status=:status AND email=:email"
    return database.execute(query, values={'status': current_user.status, 'email': current_user.email})

def change_password(
    change_password_object: user_schema.ChangePassword,
    current_user: auth_schema.UserList
):
    query = "UPDATE py_users SET password=:password WHERE status='1' AND email=:email"
    return database.execute(query, values={'password':change_password_object.new_password, 'email': current_user.email})

def save_black_list_token(
    token: str,
    current_user: auth_schema.UserList
):
    query = 'INSERT INTO py_blacklists VALUES (:token, :email)'
    return database.execute(query, values={"token": token, "email": current_user.email})