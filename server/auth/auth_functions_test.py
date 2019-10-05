from server.auth import auth_functions as auth
from server.message import message_functions as message
import pytest

# Testing Functions
def test_auth_login():
    # A registered user is logged in
    assert auth.auth_login("registered_email", "registered_password") \
         == {"u_id": "valid_u_id", "token": "valid_token"}
    # An invalid email is given
    with pytest.raises(ValueError, match = "Invalid Email"):
        auth.auth_login("invalid_email", "valid_password")
    # Email is not a registered email
    with pytest.raises(ValueError, match = "Email not registered"):
        auth.auth_login("unregistered_email", "valid_password")
    # Password is incorrect
    with pytest.raises(ValueError, match = "Password Incorrect"):
        auth.auth_login("registered_email", "invalid_password")

def test_auth_logout():
    # A user is registered
    login_details = auth.auth_register("valid_correct_email",  \
        "valid_correct_password", "valid_first_name", "valid_last_name")

    #Confirming user is logged in
    assert message.message_send(login_details["token"], 1, "Hi") == {}
    
    # User is logged out, sending message will now raise token error
    with pytest.raises(KeyError, match = "token"):
        login_details = auth.auth_logout(login_details)
        message.message_send(login_details["token"], 1, "Hi")

def test_auth_register():
    #A user is registered
    assert auth.auth_register("valid_correct_email", "valid_correct_password", \
         "valid_correct_first_name", "valid_correct_last_name") \
              == {"u_id": "valid_u_id", "token": "valid_token"}

    # A invalid email is given
    with pytest.raises(ValueError, match = "Invalid Email"):
        auth.auth_register("invalid_email", "valid_password", \
             "valid_first_name", "valid_last_name")
    # Email given is already in use
    with pytest.raises(ValueError, match = "Email Already Registered"):
        auth.auth_register("registered_email", "valid_password", \
             "valid_first_name", "valid_last_name")
    # Password provided is not strong enough
    with pytest.raises(ValueError, match = "Password Not Strong"):
        auth.auth_register("valid_correct_email", "invalid_password", \
             "valid_first_name", "valid_last_name")
    # First name is invalid
    with pytest.raises(ValueError, match = "Invalid First Name"):
        auth.auth_register("valid_correct_email", "valid_correct_password", \
             "invalid_first_name", "valid_last_name")
    # Last name is invalid
    with pytest.raises(ValueError, match = "Invalid Last Name"):
        auth.auth_register("valid_correct_email", "valid_correct_password", \
             "valid_first_name", "invalid_last_name")

def test_auth_passwordreset_request():
    # Password reset request is sent to valid email
    assert auth.auth_passwordreset_request("valid_email") == {}

def test_auth_passwordreset_reset():
    # Password is reset when valid reset code and password is given
    auth.auth_passwordreset_reset("valid_reset_code", "valid_correct_password")
    # Reset code is invalid
    with pytest.raises(ValueError, match = "Invalid Reset Code"):
        auth.auth_passwordreset_reset("invalid_reset_code", "valid_password")
    # Invalid password is given
    with pytest.raises(ValueError, match = "Invalid Password"):
        auth.auth_passwordreset_reset("valid_reset_code", "invalid_password")