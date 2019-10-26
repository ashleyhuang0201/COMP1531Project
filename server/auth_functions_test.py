'''
Test functions for auth_*
'''
import pytest
import server.auth_functions as auth
import server.message_functions as message

# Testing Functions
def test_auth_login():
    '''
    Test functions for auth_login
    '''
    # A registered user is logged in
    login = auth.auth_login("registered@g.com", "registered_password") \

    # Check database for id and token
    user_id = get_u_id("registered@g.com")
    user_token = get_token(user_id)

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
    # A user is registered
    login_details = auth.auth_register("validcorrect@g.com",  \
        "valid_correct_password", "valid_first_name", "valid_last_name")

    #Confirming user is logged in
    assert message.message_send(login_details["token"], 1, "Hi") == {}

    # User is logged out, sending message will now raise token error
    with pytest.raises(KeyError, match="token"):
        login_details = auth.auth_logout(login_details)
        message.message_send(login_details["token"], 1, "Hi")

def test_auth_register():
    '''
    Test functions for auth_register
    '''
    #A user is registered
    reg_result = auth.auth_register("validcorrect@g.com", "valid_password", \
         "valid_correct_first_name", "valid_correct_last_name")

    # Check database for id and token
    user_id = get_u_id("validcorrect@g.com")
    user_token = get_token(user_id)

    # confirm that register returned the correct ID and token
    assert reg_result == {"u_id": user_id, "token": user_token}

    # A invalid email is given
    with pytest.raises(ValueError, match="Invalid Email"):
        auth.auth_register("invalid_email", "valid_password", \
             "valid_first_name", "valid_last_name")
    # Email given is already in use
    with pytest.raises(ValueError, match="Email Already Registered"):
        auth.auth_register("registered@g.com", "valid_password", \
             "valid_first_name", "valid_last_name")
    # Password provided is not strong enough
    with pytest.raises(ValueError, match="Password Not Strong"):
        auth.auth_register("validcorrect@g.com", "bpas", \
             "valid_first_name", "valid_last_name")
    # First name is invalid
    with pytest.raises(ValueError, match="Invalid First Name"):
        auth.auth_register("validcorrect@g.com", "valid_correct_password", \
             "invalid_first_name", "valid_last_name")
    # Last name is invalid
    with pytest.raises(ValueError, match="Invalid Last Name"):
        auth.auth_register("validcorrect@g.com", "valid_correct_password", \
             "valid_first_name", "invalid_last_name")

def test_auth_passwordreset_request():
    '''
    Test functions for auth_passwordreset_request
    '''
    # Password reset request is sent to valid email
    assert auth.auth_passwordreset_request("vali@g.com") == {}

def test_auth_passwordreset_reset():
    '''
    Test functions for auth_passwordreset_reset
    '''
    # Password is reset when valid reset code and password is given
    auth.auth_passwordreset_reset(get_code("vali@g.com"), "valid_password")
    # Reset code is invalid
    with pytest.raises(ValueError, match="Invalid Reset Code"):
        auth.auth_passwordreset_reset("invalid_reset_code", "valid_password")
    # Invalid password is given
    with pytest.raises(ValueError, match="Invalid Password"):
        auth.auth_passwordreset_reset(get_code("vali@g.com"), "bpas")

# helper function that accesses database to get the user ID given an email
def get_u_id(email):
    '''
    Helper
    '''
    u_id = 1
    return u_id

# helper function to get the token of a user from u_id
def get_token(u_id):
    '''
    Helper
    '''
    token = 'valid_token'
    return token

# Get the reset code that was sent to email
def get_code(email):
    '''
    Helper
    '''
    return "valid_reset_code"
