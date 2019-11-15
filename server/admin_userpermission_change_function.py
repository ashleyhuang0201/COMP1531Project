'''
Admin Functions
admin_userpermission_change: Change user's permission
'''
from server.Error import AccessError, ValueError
import server.global_var as global_var
from server.helpers import valid_token, valid_user_id, valid_permission_id, \
     token_is_admin, token_is_owner, get_user_by_u_id

@valid_token
def admin_userpermission_change(token, u_id, permission_id):
    '''
    Given a User by their user ID, set their permissions to new permissions
    described by permission_id
    '''
    # Checking validity of permission change request
    if not valid_user_id(u_id):
        raise ValueError('User ID is invalid')
    if not valid_permission_id(permission_id):
        raise ValueError('Permission ID is invalid')
    if not (token_is_admin(token) or token_is_owner(token)):
        raise AccessError('Current user is not an admin or owner')

    user = get_user_by_u_id(u_id)
    user.change_permissions(permission_id)

    return {}
