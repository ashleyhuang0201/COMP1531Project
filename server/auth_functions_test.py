'''
Test functions for auth_*
'''
import pytest

import server.auth_functions as auth
import server.channel_functions as channel
import server.global_var as data
from server.Error import AccessError, ValueError
from server.helpers import (get_reset_code_from_email, get_user_by_email,
                            get_user_by_token, get_user_token_by_u_id)


# Testing Functions
def test_auth_login():
    '''
    Test functions for auth_login
    '''

    data.initialise_all()

    # Register a user and then log in
    auth.auth_register("registered@g.com", "registered_password", "a", "b")

    # A registered user is logged in
    login = auth.auth_login("registered@g.com", "registered_password") \

    # Check database for id and token
    user_id = get_user_by_email("registered@g.com").u_id
    user_token = get_user_token_by_u_id(user_id)

    assert login == {"u_id": user_id, "token": user_token}

    # An invalid email is given
    with pytest.raises(ValueError, match="Invalid Email"):
        auth.auth_login("invalid_email", "valid_password")
    # Email is not a registered email
    with pytest.raises(ValueError, match="Email not registered"):
        auth.auth_login("unregistered_email@g.com", "valid_password")
    # Password is incorrect
    with pytest.raises(ValueError, match="Password Incorrect"):
        auth.auth_login("registered@g.com", "bpas")

def test_auth_logout():
    '''
    Test functions for auth_logout
    '''

    data.initialise_all()

    # Test logging out a rubbish token
    assert auth.auth_logout("bad") == {"is_success": False}

    # A user is registered
    user = auth.auth_register("validcorrect@g.com", "valid_password", "a", "b")

    #Confirming user is logged in
    assert channel.channels_create(user["token"], "testing", False) == {
        "channel_id": 0
    }

    # User is logged out, creating channel will now raise token error
    assert auth.auth_logout(user["token"]) == {"is_success": True}
    with pytest.raises(AccessError, match="token"):
        channel.channels_create(user["token"], "testing2", True)

def test_auth_register():
    '''
    Test functions for auth_register
    '''

    data.initialise_all()

    #A user is registered
    user = auth.auth_register("registered@g.com", "valid_password", "a", "b")

    # Check database for id and token
    user_id = get_user_by_email("registered@g.com").u_id
    user_token = get_user_token_by_u_id(user_id)

    # confirm that register returned the correct ID and token
    assert user == {"u_id": user_id, "token": user_token}

    # A invalid email is given
    with pytest.raises(ValueError, match="Invalid Email"):
        auth.auth_register("invalid_email", "valid_password", "a", "b")
    # Email given is already in use
    with pytest.raises(ValueError, match="Email Already Registered"):
        auth.auth_register("registered@g.com", "valid_password", "a", "b")
    # Password provided is not strong enough
    with pytest.raises(ValueError, match="Password Not Strong"):
        auth.auth_register("validcorrect@g.com", "bpas", "a", "b")
    # First name is invalid
    with pytest.raises(ValueError, match="Invalid First Name"):
        invalid = "a" * 51
        auth.auth_register("validcorrect@g.com", "valid_password", invalid, "b")
    # Last name is invalid
    with pytest.raises(ValueError, match="Invalid Last Name"):
        auth.auth_register("validcorrect@g.com", "valid_password", "a", invalid)

    # Testing unique handle
    # Creating user: first_name="asd", last_name="dsa"
    user1 = auth.auth_register("g@g.com", "valid_password", "asd", "dsa")
    user1 = get_user_by_token(user1["token"])
    assert user1.handle == "asddsa"

    # Creating user: first_name="asd", last_name="dsa"
    user2 = auth.auth_register("a@g.com", "valid_password", "asd", "dsa")
    user2 = get_user_by_token(user2["token"])
    assert user2.handle == "2asddsa"

def test_auth_passwordreset_request():
    '''
    Test functions for auth_passwordreset_request
    '''

    data.initialise_all()

    # Create account to be password reset request
    auth.auth_register("comp1531receive@gmail.com", "valid_password", "a", "b")

    # Password reset request is sent to valid email
    auth.auth_passwordreset_request("comp1531receive@gmail.com")

    # Password reset request is sent to invalid email
    with pytest.raises(ValueError, match="Email is not valid"):
        auth.auth_passwordreset_request("comp1531receive.com")

def test_auth_passwordreset_reset():
    '''
    Test functions for auth_passwordreset_reset
    '''

    data.initialise_all()

    # Create account to be password reset request
    auth.auth_register("comp1531receive@gmail.com", "valid_password", "a", "b")

    # Password reset request is sent to valid email
    auth.auth_passwordreset_request("comp1531receive@gmail.com")

    # Password is reset when valid reset code and password is given
    reset_code = get_reset_code_from_email("comp1531receive@gmail.com")
    auth.auth_passwordreset_reset(reset_code, "new_password")
    # Reset code is invalid
    with pytest.raises(ValueError, match="Invalid Reset Code"):
        auth.auth_passwordreset_reset("invalid_reset_code", "valid_password")
    # Invalid password is given
    with pytest.raises(ValueError, match="Invalid Password"):
        auth.auth_passwordreset_reset(reset_code, "bpas")
