# Tests for the permission change function function
# Created by: Coen Townson
# Created on: 3/10/2019

import pytest
from server.admin.admin_userpermission_change_function import \
    admin_userpermission_change
from server.helper.valid_checks import valid_user_id
from server.helper.permission_checks import token_is_admin, token_is_owner
from server.auth.auth_functions import auth_register

user_admin = auth_register("test@gmail.com", "pass123", "Rayden", "Smith")
token_admin = user_admin["token"]
u_id_admin = user_admin["u_id"]

user = auth_register("test2@gmail.com", "pass123", "Rayden", "Smith")
token_user = user["token"]

def test_invalid_user():
    with pytest.raises(ValueError, match = 'User ID is invalid'):
        admin_userpermission_change(token_admin, -1, 1)

def test_invalid_permission():
    with pytest.raises(ValueError, match = 'Permission ID is invalid'):
        admin_userpermission_change(token_admin, 1, 0)

def test_user_member():
    with pytest.raises(ValueError, match = \
        'Current user is not an admin or owner'):
        admin_userpermission_change(token_user, 1, 1)

def test_invalid_token():
    with pytest.raises(ValueError, match = 'Invalid token'):
        admin_userpermission_change('invalid token', 1, 1)

# Below cases should pass - this will be completed when we can 
# generate the tokens correctly

def test_user_admin():
    assert admin_userpermission_change(token_admin, 1, 1) == {}
