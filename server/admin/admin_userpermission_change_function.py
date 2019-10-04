# Dummy implementation for permission change function
# Created by: Coen Townson
# Created on: 3/10/2019

from server.helper.Error import AccessError
from server.helper.valid_checks import valid_user_id, valid_token
from server.helper.permission_checks import token_is_admin, token_is_owner

def admin_userpermission_change(token, u_id, permission_id):
    if (not valid_user_id(u_id)):
        raise ValueError('User ID is invalid')
    if (permission_id > 3 or permission_id < 1):
        raise ValueError('Permission ID is invalid')
    if (not valid_token(token)):
        raise AccessError('Invalid token')
    if (not (token_is_admin(token) or token_is_owner(token))):
        raise AccessError('Current user is not an admin or owner')
    
    return {}