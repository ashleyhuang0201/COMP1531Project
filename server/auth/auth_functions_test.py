from . import auth_functions as auth
from ..message import message_functions as message
import pytest

# Testing Functions
def test_auth_login():
    assert auth.auth_login("registered_email", "registered_password") == {"u_id": "valid_u_id", "token": "valid_token"}

    with pytest.raises(ValueError, match = "Invalid Email"):
        auth.auth_login("invalid_email", "valid_password")
    with pytest.raises(ValueError, match = "Email not registered"):
        auth.auth_login("unregistered_email", "valid_password")
    with pytest.raises(ValueError, match = "Password Incorrect"):
        auth.auth_login("registered_email", "invalid_password")

def test_auth_logout():
    login_details = auth.auth_register("valid_correct_email", "valid_correct_password", "valid_first_name", "valid_last_name")

    assert message.message_send(login_details["token"], 1, "Hi") == {}
    
    with pytest.raises(KeyError, match = "token"):
        login_details = auth.auth_logout(login_details)
        message.message_send(login_details["token"], 1, "Hi")

def test_auth_register():
    assert auth.auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name") == {"u_id": "valid_u_id", "token": "valid_token"}

    with pytest.raises(ValueError, match = "Invalid Email"):
        auth.auth_register("invalid_email", "valid_password", "valid_first_name", "valid_last_name")
    with pytest.raises(ValueError, match = "Email Already Registered"):
        auth.auth_register("registered_email", "valid_password", "valid_first_name", "valid_last_name")
    with pytest.raises(ValueError, match = "Password Not Strong"):
        auth.auth_register("valid_correct_email", "invalid_password", "valid_first_name", "valid_last_name")
    with pytest.raises(ValueError, match = "Invalid First Name"):
        auth.auth_register("valid_correct_email", "valid_correct_password", "invalid_first_name", "valid_last_name")
    with pytest.raises(ValueError, match = "Invalid Last Name"):
        auth.auth_register("valid_correct_email", "valid_correct_password", "valid_first_name", "invalid_last_name")

def test_auth_passwordreset_request():
    assert auth.auth_passwordreset_request("valid_email") == {}

def test_auth_passwordreset_reset():
    auth.auth_passwordreset_reset("valid_reset_code", "valid_correct_password")
    with pytest.raises(ValueError, match = "Invalid Reset Code"):
        auth.auth_passwordreset_reset("invalid_reset_code", "valid_password")
    with pytest.raises(ValueError, match = "Invalid Password"):
        auth.auth_passwordreset_reset("valid_reset_code", "invalid_password")