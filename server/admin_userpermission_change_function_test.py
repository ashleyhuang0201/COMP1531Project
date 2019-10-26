"""
Tests for admin
admin_userpermission_change: Invalid user, invalid permission, user_member,
invalid_token, successful case (permission changes by owner and admin, ability
to change permission to any three states)
"""
import pytest
from server.admin_userpermission_change_function import \
    admin_userpermission_change
from server.helpers import valid_user_id, token_is_admin, token_is_owner, get_user_token_by_u_id, get_user_by_u_id
from server.auth_functions import auth_register
from server.Error import AccessError
import server.global_var as global_var

# Invalid token
def test_invalid_token():
    with pytest.raises(AccessError, match = 'Invalid token'):
        # Initialising
        global_var.initialise_all()

        # Creating a valid user who can change permissions
        user = auth_register("test@gmail.com", "pass123", "Rayden", "Smith")
        get_user_by_u_id(user["u_id"]).permission = 1
        
        admin_userpermission_change("invalid token", user["u_id"], 2)

# Invalid user_id
def test_invalid_user_id():
    with pytest.raises(ValueError, match = 'User ID is invalid'):
        # Initialising
        global_var.initialise_all()

        # Creating a valid user who can change permissions
        user = auth_register("test@gmail.com", "pass123", "Rayden", "Smith")
        get_user_by_u_id(user["u_id"]).permission = 1
        
        admin_userpermission_change(get_user_token_by_u_id(user["u_id"]), -1, 2)

# Invalid permission
def test_invalid_permission():
    with pytest.raises(ValueError, match = 'Permission ID is invalid'):
        # Initialising
        global_var.initialise_all()

        # Creating a valid user who can change permissions
        user = auth_register("test@gmail.com", "pass123", "Rayden", "Smith")
        get_user_by_u_id(user["u_id"]).permission = 1

        admin_userpermission_change(get_user_token_by_u_id(user["u_id"]), user["u_id"], -1)

# Invalid user
def test_user_member():
    with pytest.raises(AccessError, match = 'Current user is not an admin or owner'):
        # Initialising
        global_var.initialise_all()

        # Creating a user who cannot change permissions
        user = auth_register("test@gmail.com", "pass123", "Rayden", "Smith")
        get_user_by_u_id(user["u_id"]).permission = 3

        admin_userpermission_change(get_user_token_by_u_id(user["u_id"]), user["u_id"], 1)

# Successful permission change by admin
def test_user_admin():
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

# Successful permission change by owner
def test_user_owner():
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

# Ability to change permission to user, owner and admin
def test_user_permission_possible_permissions():
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
