# Tests for the permission change function function
# Created by: Coen Townson
# Created on: 3/10/2019

import pytest
from server.admin.admin_userpermission_change_function import admin_userpermission_change
from server.helper.valid_checks import (
    valid_user_id, 
    token_is_admin, 
    token_is_owner
)

def test_invalid_user():
    with pytest.raises(ValueError, match = 'User ID is invalid'):
        admin_userpermission_change('valid token', -1, 1)

def test_invalid_permission():
    with pytest.raises(ValueError, match = 'Permission ID is invalid'):
        admin_userpermission_change('valid token', 1, 0)

def test_user_member():
    with pytest.raises(ValueError, match = 'Current user is not an admin or owner'):
        admin_userpermission_change('token of a member', 1, 1)

def test_invalid_token():
    with pytest.raises(ValueError, match = 'Invalid token'):
        admin_userpermission_change('invalid token', 1, 1)

# Below cases should pass - this will be completed when we can generate the tokens correctly

def test_user_admin():
    assert admin_userpermission_change('token of an admin', 1, 1) == {}

def test_user_owner():
    assert admin_userpermission_change('token of an owner', 1, 1) == {}
