import auth_functions as ph2 # Getting functions # Change ph2 to something else

# Testing Functions
def test_auth_login():
    # Valid login
    assert ph2.auth_login("test@gmail.com", "password") == ("u_id", "123456"), "valid email and valid password"
    # Invalid email
    assert ph2.auth_login("test", "password") != ("u_id", "123456"), "invalid email"
    # Invalid password
    assert ph2.auth_login("test@gmail.com", "pass") != ("u_id", "123456"), "invalid password"
    # Email not associated with user
    assert ph2.auth_login("test1@gmail.com", "password") != ("u_id", "123456"), "invalid user"
    # Password not associated with email
    assert ph2.auth_login("test@gmail.com", "wrongpassword") != ("u_id", "123456"), "invalid password to user"
    # No entry
    assert ph2.auth_login("", "") != ("u_id", "123456"), "no entry"

def test_auth_logout():
    # How to test successful logout?
    pass

def test_auth_register():
    pass
    # Valid login
    assert ph2.auth_register("test@gmail.com", "password", "firstname", "lastname") == ("u_id", "123456"), "valid login"
    # Invalid email
    assert ph2.auth_register("test1@gmail.com", "password", "firstname", "lastname") != ("u_id", "123456"), "invalid email"
    # Invalid password
    assert ph2.auth_register("test@gmail.com", "ps", "firstname", "lastname") != ("u_id", "123456"), "invalid password"
    # Invalid first name
    assert ph2.auth_register("test@gmail.com", "password", "00110001001100100011001100110100001101010011011000110111", "lastname") != ("u_id", "123456"), "invalid first name"
    # Invalid last name
    assert ph2.auth_register("test@gmail.com", "password", "firstname", "00110001001100100011001100110100001101010011011000110111") != ("u_id", "123456"), "invalid last name"
    # No entry
    assert ph2.auth_register("", "", "", "") != ("u_id", "123456"), "no entry"

def test_auth_passwordreset_request():
    # Valid email
    ph2.auth_passwordreset_request("test@gmail.com")
    # Invalid email
    ph2.auth_passwordreset_request("invalid@gmail.com")

def test_auth_passwordreset_reset():
    # Valid reset code and password
    # Invalid reset code
    # Invalid password
    pass