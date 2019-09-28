import functions as ph2 # Getting functions # Change ph2 to something else

# Testing
def test_auth_login():
    # Valid login
    assert ph2.auth_login("test@gmail.com", "password") == "123456", "email: 'test@gmail.com' and password: 'password' passes - valid email and valid password"
    # Invalid email
    assert ph2.auth_login("test", "password") != "123456", "email: 'test' and password: 'password' fails - invalid email"
    # Invalid password
    assert ph2.auth_login("test@gmail.com", "pass") != "123456", "email: 'test@gmail.com' and password: 'pass' fails - invalid password"
    # Invalid email and invalid password
    assert ph2.auth_login("test", "pass") != "123456", "email: 'test' and password: 'pass' fails - invalid email and invalid password"
    # Email not associated with user
    assert ph2.auth_login("test1@gmail.com", "password") != "123456", "email: 'test1@gmail.com' and password: 'password' fails - invalid user"
    # No entry
    assert ph2.auth_login("", "") != "123456", "email: '' and password: '' fails - no entry"