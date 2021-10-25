from fastapi import APIRouter, Depends, status, HTTPException
from api.auth import schema as auth_schema, crud as auth_crud
from api.users import schema as user_schema, crud as user_crud
from api.utils import jwt_util, crypto_util



router = APIRouter(
    prefix="/api/v1"
)

@router.get('/user/profile')
async def get_user_profile(current_user: auth_schema.UserList = Depends(jwt_util.get_current_active_user)):
    return current_user 

@router.patch("/user/profile")
async def update_profile(
    request: user_schema.UserUpdate,
    current_user: auth_schema.UserList = Depends(jwt_util.get_current_user)
):
    # Update User Info
    await user_crud.update_user(request, current_user)

    return {
        'status_code': status.HTTP_200_OK,
        'detail': 'User Updated Successfully'
    }


@router.delete('/user/profile')
async def deactivate_account(
    current_user: auth_schema.UserList = Depends(jwt_util.get_current_active_user)
):
 
    # Delete user
    await crud.deactivate_user(current_user)
    return {
        'status_code': status.HTTP_200_OK,
        'detail': 'User Account Has Been Deactivated Successfully'
    }

@router.patch("/user/change-password")
async def change_password(
    change_password_object: user_schema.ChangePassword,
    current_user: auth_schema.UserList = Depends(jwt_util.get_current_active_user)
):
    # Cehck User
    result = await auth_crud.find_user_exist(current_user.email)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Found')
    
    # Verify Password
    user = auth_schema.UserCreate(**result)
    valid = crypto_util.verify_password(change_password_object.current_password, user.password)
    if not valid:
        raise HTTPException(statu_code=status.HTTP_401_UNAUTHORIZED, detail="Current Password Is Not Match")
    
    # Check new password and confirm password
    if change_password_object.new_password != change_password_object.confirm_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='New Password Not Match')

    # Change Password
    change_password_object.new_password = crypto_util.hash_password(change_password_object.new_password)
    await user_crud.change_password(change_password_object, current_user)

    return {
        'status_code':status.HTTP_200_OK,
        'detail': 'Password Has Been Change Successfully',
    }

@router.get('/user/logout')
async def logout(
    token: str = Depends(jwt_util.get_token_user),
    current_user: auth_schema.UserList = Depends(jwt_util.get_current_active_user)
):
    # Save token of user to table blacklist
    result = await user_crud.save_black_list_token(token, current_user)
    return {
        'status_code': status.HTTP_200_OK,
        'detail': 'User Logged Out Successfully'
    }