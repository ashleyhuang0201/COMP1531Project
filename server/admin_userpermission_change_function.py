'''
Team: You_Things_Can_Choose
Admin Functions
admin_userpermission_change: Change user's permission
'''
from server.Error import AccessError, ValueError
from server.helpers import (get_user_by_u_id, token_is_admin, token_is_owner,
                            valid_permission_id, valid_token)

@valid_token
def admin_userpermission_change(token, u_id, permission_id):
    '''
    Given a User by their user ID, set their permissions to new permissions
    described by permission_id
    '''

    # Getting user object
    user = get_user_by_u_id(u_id)

    # Checking validity of permission change request
    if not user:
        raise ValueError('Invalid User ID')
    if not valid_permission_id(permission_id):
        raise ValueError('Permission ID is invalid')
    if not (token_is_admin(token) or token_is_owner(token)):
        raise AccessError('Current user is not an admin or owner')

    # Changing user's permission
    user.change_permissions(permission_id)

    return {}
