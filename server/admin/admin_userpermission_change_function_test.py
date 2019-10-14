'''
Tests for the permission change function function
Created by: Coen Townson
Created on: 3/10/2019
'''
import pytest
from server.admin.admin_userpermission_change_function import \
    admin_userpermission_change
from server.auth.auth_functions import auth_register

USER_ADMIN = auth_register("test@gmail.com", "pass123", "Rayden", "Smith")
TOKEN_ADMIN = USER_ADMIN["token"]
U_ID_ADMIN = USER_ADMIN["u_id"]

USER = auth_register("test2@gmail.com", "pass123", "Rayden", "Smith")
TOKEN_USER = USER["token"]

def test_invalid_user():
    '''
    Tests invalid user case
    '''
    with pytest.raises(ValueError, match='User ID is invalid'):
        admin_userpermission_change(TOKEN_ADMIN, -1, 1)

def test_invalid_permission():
    '''
    Tests invalid permission value case
    '''
    with pytest.raises(ValueError, match='Permission ID is invalid'):
        admin_userpermission_change(TOKEN_ADMIN, 1, 0)

def test_user_member():
    '''
    Tests invalid user permissions case
    '''
    with pytest.raises(ValueError, match=\
        'Current user is not an admin or owner'):
        admin_userpermission_change(TOKEN_USER, 1, 1)

def test_invalid_token():
    '''
    Tests invalid token case
    '''
    with pytest.raises(ValueError, match='Invalid token'):
        admin_userpermission_change('invalid token', 1, 1)

# Below cases should pass - this will be completed when we can
# generate the tokens correctly

def test_user_admin():
    '''
    Tests valid case
    '''
    assert admin_userpermission_change(TOKEN_ADMIN, 1, 1) == {}
