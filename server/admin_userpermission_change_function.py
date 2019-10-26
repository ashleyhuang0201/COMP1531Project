"""
Admin Functions
admin_userpermission_change: Change user's permission
"""
from server.Error import AccessError
import server.helpers as helper

def admin_userpermission_change(token, u_id, permission_id):
    """
    Given a User by their user ID, set their permissions to new permissions
    described by permission_id
    """
    # Checking validity of permission change request
    if not helper.valid_token(token):
        raise AccessError('Invalid token')
    if not helper.valid_user_id(u_id):
        raise ValueError('User ID is invalid')
    if not helper.valid_permission_id(permission_id):
        raise ValueError('Permission ID is invalid')
    if not (helper.token_is_admin(token) or helper.token_is_owner(token)):
        raise AccessError('Current user is not an admin or owner')

    user = helper.get_user_by_u_id(u_id)
    user.change_permissions(permission_id)

    return {}
