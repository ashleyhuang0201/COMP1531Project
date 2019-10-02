import auth_functions as auth
import pytest

# Testing Functions
def test_auth_login():
    # Valid login
    assert auth.auth_login("registered_email", "registered_password") == ("valid_u_id", "valid_token")

    with pytest.raises(ValueError, match = "Invalid Details"):
        auth.auth_login("invalid_email", "valid_password") # Invalid email
    with pytest.raises(ValueError, match = "Invalid Details"):
        auth.auth_login("incorrect_email", "valid_password") # Invalid User
    with pytest.raises(ValueError, match = "Invalid Details"):
        auth.auth_login("valid_correct_email", "invalid_password") # Wrong password

def test_auth_logout():
    pass

def test_auth_register():
    # Valid Register
    assert auth.auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name") == ("valid_u_id", "valid_token")

    with pytest.raises(ValueError, match = "Invalid Details"):
        auth.auth_register("invalid_email", "valid_password", "valid_first_name", "valid_last_name") # Invalid email
    with pytest.raises(ValueError, match = "Invalid Details"):
        auth.auth_register("used_email", "valid_password", "valid_first_name", "valid_last_name") # Used email
    with pytest.raises(ValueError, match = "Invalid Details"):
        auth.auth_register("valid_correct_email", "invalid_password", "valid_first_name", "valid_last_name") # Invalid password
    with pytest.raises(ValueError, match = "Invalid Details"):
        auth.auth_register("valid_correct_email", "valid_correct_password", "invalid_first_name", "valid_last_name") # Invalid first name
    with pytest.raises(ValueError, match = "Invalid Details"):
        auth.auth_register("valid_correct_email", "valid_correct_password", "valid_first_name", "invalid_last_name") # Invalid last name

def test_auth_passwordreset_request():
    pass

def test_auth_passwordreset_reset():
    # Valid reset
    auth.auth_passwordreset_reset("valid_reset_code", "valid_correct_password")

    with pytest.raises(ValueError, match = "Invalid Details"):
        auth.auth_passwordreset_reset("invalid_reset_code", "valid_password") # Invalid reset code
    with pytest.raises(ValueError, match = "Invalid Details"):
        auth.auth_passwordreset_reset("valid_reset_code", "invalid_password") # Invalid password