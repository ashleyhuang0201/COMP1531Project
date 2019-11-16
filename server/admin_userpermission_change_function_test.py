"""
Tests for admin
admin_userpermission_change: Invalid user, invalid permission, user_member,
invalid_token, successful case (permission changes by owner and admin, ability
to change permission to any three states)
"""
import pytest

import server.global_var as global_var
from server.admin_userpermission_change_function import \
    admin_userpermission_change
from server.auth_functions import auth_register
from server.constants import SLACKR_ADMIN, SLACKR_OWNER, SLACKR_USER
from server.Error import AccessError, ValueError
from server.helpers import (get_user_by_u_id, get_user_token_by_u_id,
                            valid_token)


# Invalid token for admin_userpermission_change
def test_admin_userpermission_change_invalid_token():
    '''
    Checks when an invalid token is sent to admin_userpermission_change
    '''
    with pytest.raises(AccessError, match='Invalid token'):
        # Initialising
        global_var.initialise_all()

        # Creating a valid user who can change permissions
        user = auth_register("test@gmail.com", "pass123", "Rayden", "Smith")
        get_user_by_u_id(user["u_id"]).permission = SLACKR_USER

        # Calling admin_userpermission_change with an invalid token
        admin_userpermission_change("invalid token", \
                                                 user["u_id"], SLACKR_ADMIN)

# Invalid user_id for admin_userpermission_change
def test_admin_userpermission_change_invalid_user_id():
    '''
    Checks when an invalid user id is sent to admin_userpermission_change
    '''
    with pytest.raises(ValueError, match='Invalid User ID'):
        # Initialising
        global_var.initialise_all()

        # Creating a valid user who can change permissions
        user = auth_register("test@gmail.com", "pass123", "Rayden", "Smith")
        get_user_by_u_id(user["u_id"]).permission = SLACKR_OWNER

        # Calling admin_userpermission_change with an invalid user id
        admin_userpermission_change(get_user_token_by_u_id(user["u_id"]), \
                                                -1, SLACKR_ADMIN)

# Invalid permission for admin_userpermission_change
def test_admin_userpermission_change_invalid_permission():
    '''
    Checks when an invalid permission is sent to admin_userpermission_change
    '''
    with pytest.raises(ValueError, match='Permission ID is invalid'):
        # Initialising
        global_var.initialise_all()

        # Creating a valid user who can change permissions
        user = auth_register("test@gmail.com", "pass123", "Rayden", "Smith")
        get_user_by_u_id(user["u_id"]).permission = SLACKR_OWNER

        # Calling admin_userpermission_change with an invalid permission
        admin_userpermission_change(get_user_token_by_u_id(user["u_id"]), \
                                                         user["u_id"], -1)

# Invalid user for admin_userpermission_change
def test_admin_userpermission_change_user_member():
    '''
    Checks when an unauthorised user is sent to admin_userpermission_change
    '''
    with pytest.raises(AccessError, \
                                 match='Current user is not an admin or owner'):
        # Initialising
        global_var.initialise_all()

        # Creating a user who cannot change permissions
        user = auth_register("test@gmail.com", "pass123", "Rayden", "Smith")
        get_user_by_u_id(user["u_id"]).permission = SLACKR_USER

        # Calling admin_userpermission_change with a normal 'user' user
        admin_userpermission_change(get_user_token_by_u_id(user["u_id"]), \
                                             user["u_id"], SLACKR_OWNER)

# Successful permission change by admin for admin_userpermission_change
def test_admin_userpermission_change_user_admin():
    '''
    Testing successful case of changing permissions by an admin of slackr
    '''
    # Initialising
    global_var.initialise_all()

    # Creating a valid admin who can change permissions
    admin1 = auth_register("admin1@gmail.com", "pass123", "Rayden", "Smith")
    get_user_by_u_id(admin1["u_id"]).permission = SLACKR_ADMIN

    # Creating normal member
    user = auth_register("member@gmail.com", "pass123", "Rayden", "Smith")
    get_user_by_u_id(user["u_id"]).permission = SLACKR_USER

    # Creating another admin
    admin2 = auth_register("admin2@gmail.com", "pass123", "Rayden", "Smith")
    get_user_by_u_id(admin2["u_id"]).permission = SLACKR_ADMIN

    # Creating another owner
    owner = auth_register("owner@gmail.com", "pass123", "Rayden", "Smith")
    get_user_by_u_id(owner["u_id"]).permission = SLACKR_OWNER

    # Admin changing permission of member
    admin_userpermission_change(get_user_token_by_u_id(admin1["u_id"]), \
                                                 user["u_id"], SLACKR_OWNER)
    assert get_user_by_u_id(user["u_id"]).permission == SLACKR_OWNER

    # Admin changing permission of another admin
    admin_userpermission_change(get_user_token_by_u_id(admin1["u_id"]), \
                                             admin2["u_id"], SLACKR_OWNER)
    assert get_user_by_u_id(admin2["u_id"]).permission == SLACKR_OWNER

    # Admin changing permission of owner
    admin_userpermission_change(get_user_token_by_u_id(admin1["u_id"]), \
                                             owner["u_id"], SLACKR_ADMIN)
    assert get_user_by_u_id(owner["u_id"]).permission == SLACKR_ADMIN

# Successful permission change by owner for admin_userpermission_change
def test_admin_userpermission_change_user_owner():
    '''
    Testing successful case of permission changes by an owner of slackr
    '''
    # Initialising
    global_var.initialise_all()

    # Creating a valid user who can change permissions
    owner1 = auth_register("owner1@gmail.com", "pass123", "Rayden", "Smith")
    get_user_by_u_id(owner1["u_id"]).permission = SLACKR_OWNER

    # Creating normal member
    user = auth_register("member@gmail.com", "pass123", "Rayden", "Smith")
    get_user_by_u_id(user["u_id"]).permission = SLACKR_USER

    # Creating admin
    admin = auth_register("admin@gmail.com", "pass123", "Rayden", "Smith")
    get_user_by_u_id(admin["u_id"]).permission = SLACKR_ADMIN

    # Creating another owner
    owner2 = auth_register("owner2@gmail.com", "pass123", "Rayden", "Smith")
    get_user_by_u_id(owner2["u_id"]).permission = SLACKR_OWNER

    # Owner changing permission of member
    admin_userpermission_change(get_user_token_by_u_id(owner1["u_id"]), \
                                                 user["u_id"], SLACKR_OWNER)
    assert get_user_by_u_id(user["u_id"]).permission == SLACKR_OWNER

    # Owner changing permission of another admin
    admin_userpermission_change(get_user_token_by_u_id(owner1["u_id"]), \
                                                admin["u_id"], SLACKR_OWNER)
    assert get_user_by_u_id(admin["u_id"]).permission == SLACKR_OWNER

    # Owner changing permission of owner
    admin_userpermission_change(get_user_token_by_u_id(owner1["u_id"]), \
                                                owner2["u_id"], SLACKR_ADMIN)
    assert get_user_by_u_id(owner2["u_id"]).permission == SLACKR_ADMIN


def test_admin_userpermission_change_user_permission_possible_permissions():
    '''
    Testing if it is possible to go through the entire permission set
    '''
    # Initialising
    global_var.initialise_all()

    # Creating a valid user who can change permissions
    owner = auth_register("owner@gmail.com", "pass123", "Rayden", "Smith")
    get_user_by_u_id(owner["u_id"]).permission = SLACKR_OWNER

    # Creating normal member
    user = auth_register("member@gmail.com", "pass123", "Rayden", "Smith")
    get_user_by_u_id(user["u_id"]).permission = SLACKR_USER

    # Changing normal member to admin
    admin_userpermission_change(get_user_token_by_u_id(owner["u_id"]), \
                                                user["u_id"], SLACKR_ADMIN)
    assert get_user_by_u_id(user["u_id"]).permission == SLACKR_ADMIN

    # Changing admin to owner
    admin_userpermission_change(get_user_token_by_u_id(owner["u_id"]), \
                                                user["u_id"], SLACKR_OWNER)
    assert get_user_by_u_id(user["u_id"]).permission == SLACKR_OWNER

    # Changing owner to member
    admin_userpermission_change(get_user_token_by_u_id(owner["u_id"]), \
                                                user["u_id"], SLACKR_USER)
    assert get_user_by_u_id(user["u_id"]).permission == SLACKR_USER
