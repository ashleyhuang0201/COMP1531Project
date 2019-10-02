import re

# Given a registered users' email and password and generates a valid token for the user to remain authenticated
def auth_login(email, password):
    if valid_email(email) == False:
        raise ValueError("Invalid Details") # Invalid Email
    if correct_email(email) == False:
        raise ValueError("Invalid Details") # Email does not correspond to a user
    if correct_password(email, password) == False:
        raise ValueError("Invalid Details") # Password does not correspond to email

    return ("valid_u_id", "valid_token") # Login Success

# Given an active token, invalidates the taken to log the user out. Given a non-valid token, does nothing
def auth_logout(token):
    if valid_token(token) == True:
        # Logout Process
        pass

# Given a user's first and last name, email address, and password, create a new account for them and return a new token for authentication in their session
def auth_register(email, password, name_first, name_last):
    if valid_email(email) == False:
        raise ValueError("Invalid Details") # Invalid Email
    if correct_email(email) == True:
        raise ValueError("Invalid Details") # Email already registered
    if valid_password(password) == False:
        raise ValueError("Invalid Details") # Password not strong
    if valid_name_first(name_first) == False:
        raise ValueError("Invalid Details") # Invalid first name
    if valid_name_last(name_last) == False:
        raise ValueError("Invalid Details") # Invalid last name

    return ("valid_u_id", "valid_token") # Register success

"""
Given an email address, if the user is a registered user, send's them a an 
email containing a specific secret code, that when entered in 
auth_passwordreset_reset, shows that the user trying to reset the password 
is the one who got sent this email.
"""
def auth_passwordreset_request(email):
    # Send password to associated email

    pass

# Given a reset code for a user, set that user's new password to the password provided
def auth_passwordreset_reset(reset_code, new_password):
    if valid_reset_code(reset_code) == False:
        raise ValueError("Invalid Details") # Invalid reset code
    if valid_password(new_password) == False:
        raise ValueError("Invalid Details") # Invalid password

    # Reset password

# Checks if an email is a valid email
def valid_email(email):  
    if email == "valid_correct_email" or email == "valid_email" or email == "correct_email" or email == "registered_email":
        return True
    else:
        return False

# Checks if a password is a valid password
def valid_password(password):
    if password == "valid_password" or password == "correct_password" or password == "valid_correct_password" or password == "registered_password":
        return True
    else:
        return False

# Checks if a user is a valid user
def correct_email(email):
    if email == "valid_email" or email == "correct_email" or email == "correct_valid_email" or email == "registered_email":
        return True
    else:
        return False

# Checks if first name is valid
def valid_name_first(name_first):
    if name_first == "valid_first_name" or name_first == "valid_correct_first_name":
        return True
    else:
        return False

# Checks if last name is valid
def valid_name_last(name_last):
    if name_last == "valid_last_name" or name_last == "valid_correct_last_name":
        return True
    else:
        return False

# Checks if a password is associated with the user
def correct_password(email, password):
    if email == "registered_email" and password == "registered_password":
        return True
    else:
        return False

# Checks the activeness of a token
def valid_token(token):
    if token == "valid_token":
        return True
    else:
        return False

# Checks if a reset code is valid
def valid_reset_code(reset_code):
    if reset_code == "valid_reset_code":
        return True
    else:
        return False