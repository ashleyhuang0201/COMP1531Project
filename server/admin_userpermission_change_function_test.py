"""
Tests for admin
admin_userpermission_change: Invalid user, invalid permission, user_member,
invalid_token, successful case (permission changes by owner and admin, ability
to change permission to any three states)
"""
import pytest
from server.admin_userpermission_change_function import admin_userpermission_change
from server.helpers import get_user_token_by_u_id, get_user_by_u_id
from server.auth_functions import auth_register
from server.Error import AccessError
import server.global_var as global_var

# Invalid token for admin_userpermission_change
def test_admin_userpermission_change_invalid_token():
    """
    Checks what happens if an invalid token is sent to admin_userpermission_change
    """
    with pytest.raises(AccessError, match='Invalid token'):
        # Initialising
        global_var.initialise_all()

        # Creating a valid user who can change permissions
        user = auth_register("test@gmail.com", "pass123", "Rayden", "Smith")
        get_user_by_u_id(user["u_id"]).permission = 1

        # Calling admin_userpermission_change with an invalid token
        admin_userpermission_change("invalid token", user["u_id"], 2)

# Invalid user_id for admin_userpermission_change
def test_admin_userpermission_change_invalid_user_id():
    """
    Checks what happens if an invalid user id is sent to admin_userpermission_change
    """
    with pytest.raises(ValueError, match='User ID is invalid'):
        # Initialising
        global_var.initialise_all()

        # Creating a valid user who can change permissions
        user = auth_register("test@gmail.com", "pass123", "Rayden", "Smith")
        get_user_by_u_id(user["u_id"]).permission = 1

        # Calling admin_userpermission_change with an invalid user id
        admin_userpermission_change(get_user_token_by_u_id(user["u_id"]), -1, 2)

# Invalid permission for admin_userpermission_change
def test_admin_userpermission_change_invalid_permission():
    """
    Checks what happens if an invalid permission is sent to admin_userpermission_change
    """
    with pytest.raises(ValueError, match='Permission ID is invalid'):
        # Initialising
        global_var.initialise_all()

        # Creating a valid user who can change permissions
        user = auth_register("test@gmail.com", "pass123", "Rayden", "Smith")
        get_user_by_u_id(user["u_id"]).permission = 1

        # Calling admin_userpermission_change with an invalid permission
        admin_userpermission_change(get_user_token_by_u_id(user["u_id"]), user["u_id"], -1)

# Invalid user for admin_userpermission_change
def test_admin_userpermission_change_user_member():
    """
    Checks what happens if an unauthorised user is sent to admin_userpermission_change
    """
    with pytest.raises(AccessError, match='Current user is not an admin or owner'):
        # Initialising
        global_var.initialise_all()

        # Creating a user who cannot change permissions
        user = auth_register("test@gmail.com", "pass123", "Rayden", "Smith")
        get_user_by_u_id(user["u_id"]).permission = 3

        # Calling admin_userpermission_change with a normal 'user' user
        admin_userpermission_change(get_user_token_by_u_id(user["u_id"]), user["u_id"], 1)

# Successful permission change by admin for admin_userpermission_change
def test_admin_userpermission_change_user_admin():
    """
    Testing successful case of changing permissions by an admin of slackr
    """
    # Initialising
    global_var.initialise_all()

    # Creating a valid admin who can change permissions
    admin1 = auth_register("admin1@gmail.com", "pass123", "Rayden", "Smith")
    get_user_by_u_id(admin1["u_id"]).permission = 2

    # Creating normal member
    user = auth_register("member@gmail.com", "pass123", "Rayden", "Smith")
    get_user_by_u_id(user["u_id"]).permission = 3

    # Creating another admin
    admin2 = auth_register("admin2@gmail.com", "pass123", "Rayden", "Smith")
    get_user_by_u_id(admin2["u_id"]).permission = 2

    # Creating another owner
    owner = auth_register("owner@gmail.com", "pass123", "Rayden", "Smith")
    get_user_by_u_id(owner["u_id"]).permission = 1

    # Admin changing permission of member
    admin_userpermission_change(get_user_token_by_u_id(admin1["u_id"]), user["u_id"], 1)
    assert get_user_by_u_id(user["u_id"]).permission == 1

    # Admin changing permission of another admin
    admin_userpermission_change(get_user_token_by_u_id(admin1["u_id"]), admin2["u_id"], 1)
    assert get_user_by_u_id(admin2["u_id"]).permission == 1

    # Admin changing permission of owner
    admin_userpermission_change(get_user_token_by_u_id(admin1["u_id"]), owner["u_id"], 2)
    assert get_user_by_u_id(owner["u_id"]).permission == 2

# Successful permission change by owner for admin_userpermission_change
def test_admin_userpermission_change_user_owner():
    """
    Testing successful case of permission changes by an owner of slackr
    """
    # Initialising
    global_var.initialise_all()

    # Creating a valid user who can change permissions
    owner1 = auth_register("owner1@gmail.com", "pass123", "Rayden", "Smith")
    get_user_by_u_id(owner1["u_id"]).permission = 1

    # Creating normal member
    user = auth_register("member@gmail.com", "pass123", "Rayden", "Smith")
    get_user_by_u_id(user["u_id"]).permission = 3

    # Creating admin
    admin = auth_register("admin@gmail.com", "pass123", "Rayden", "Smith")
    get_user_by_u_id(admin["u_id"]).permission = 2

    # Creating another owner
    owner2 = auth_register("owner2@gmail.com", "pass123", "Rayden", "Smith")
    get_user_by_u_id(owner2["u_id"]).permission = 1

    # Owner changing permission of member
    admin_userpermission_change(get_user_token_by_u_id(owner1["u_id"]), user["u_id"], 1)
    assert get_user_by_u_id(user["u_id"]).permission == 1

    # Owner changing permission of another admin
    admin_userpermission_change(get_user_token_by_u_id(owner1["u_id"]), admin["u_id"], 1)
    assert get_user_by_u_id(admin["u_id"]).permission == 1

    # Owner changing permission of owner
    admin_userpermission_change(get_user_token_by_u_id(owner1["u_id"]), owner2["u_id"], 2)
    assert get_user_by_u_id(owner2["u_id"]).permission == 2

# Ability to change permission to user, owner and admin for admin_userpermission_change
def test_admin_userpermission_change_user_permission_possible_permissions():
    """
    Testing if it is possible to go through the entire permission set
    """
    # Initialising
    global_var.initialise_all()

    # Creating a valid user who can change permissions
    owner = auth_register("owner@gmail.com", "pass123", "Rayden", "Smith")
    get_user_by_u_id(owner["u_id"]).permission = 1

    # Creating normal member
    user = auth_register("member@gmail.com", "pass123", "Rayden", "Smith")
    get_user_by_u_id(user["u_id"]).permission = 3

    # Changing normal member to admin
    admin_userpermission_change(get_user_token_by_u_id(owner["u_id"]), owner["u_id"], 2)

    # Changing admin to owner
    admin_userpermission_change(get_user_token_by_u_id(owner["u_id"]), owner["u_id"], 1)

    # Changing owner to member
    admin_userpermission_change(get_user_token_by_u_id(owner["u_id"]), owner["u_id"], 3)
