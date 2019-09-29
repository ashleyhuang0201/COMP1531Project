import re # Used to validate email (valid_email)

# Given functions
# Given a registered users' email and password and generates a valid token for the user to remain authenticated
def auth_login(email, password):
    if valid_user(email) == True and valid_email(email) == True and valid_password(password) == True and correct_password(email, password) == True: # Do I need to check valid_password here?
        # Login success
        return ("u_id", "123456")
    else:
        # Login failure
        # Implement failure message?
        return ("id_u", "404")

# Given an active token, invalidates the taken to log the user out. Given a non-valid token, does nothing
def auth_logout(token):
    if valid_token(token) == True:
        # Logout Process <-- Implement: Invalidate the token
        pass
    else:
        pass

# Guveb a user's first and last name, email address, and password, create a new account for them and return a new token for authentication in their session
def auth_register(email, password, name_first, name_last):
    if valid_email(email) == True and email_used(email) == False and valid_password(password) == True and valid_name_first(name_first) == True and valid_name_last(name_last) == True:
        # Account creation success
        return ("u_id", "123456")
    else:
        # Account creation failure
        return ("id_u", "404")

# Given a reset code for a user, set that user's new password to the password provided
def auth_passwordreset_request(email):
    if email_used(email) == True:
        # Send code to reset password
        pass
    else:
        # Send message that email not registered? <-- I added
        pass

# Given a reset code for a user, set that user's new password to the password provided
def auth_passwordreset_reset(reset_code, new_password):
    if valid_reset_code(reset_code) == True:
        # Valid reset code
        if valid_password(new_password) == True:
            # Valid password
            # Successfully changed psasword <-- Implement
            pass
        else:
            # Invalid password
            # Send message that password has to be valid
            pass
    else:
        # Invalid reset code
        pass

# Helper Functions
# Checks if an email is a valid email
def valid_email(email):  
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if re.search(regex, email):
        return True
    else:
        return False

# Checks if a password is a valid password
# Password must have at least 5 characters
def valid_password(password):
    if len(password) >= 5:
        # Valid password
        return True
    else:
        # Invalid password
        return False

# Checks if a user is a valid user
def valid_user(email):
    if email == "test@gmail.com":
        # Valid user
        return True
    else:
        # Invalid user
        return False

# Checks if first name is valid
def valid_name_first(name_first):
    if len(name_first) <= 50:
        # First name valid
        return True
    else:
        # First name invalid
        return False

# Checks if last name is valid
def valid_name_last(name_last):
    if len(name_last) <= 50:
        # Last name valid
        return True
    else:
        # Last name invalid
        return False

# Checks if a password is associated with the user
def correct_password(email, password):
    if email == "test@gmail.com" and (password == "" or password == "password" or password == "pass"):
        # Password is correct
        return True
    else:
        # Password is incorrect
        return False

# Checks the validity of a token
def valid_token(token):
    if token == "123456":
        # Active token
        return True
    else:
        # Inactive token
        return False

# Checks database if the email is already registered
def email_used(email):
    if email != "test@gmail.com":
        # Non-unique email
        return True
    else:
        # Unique email
        return False

# Checks if a reset code is valid
def valid_reset_code(reset_code):
    if reset_code == "1337":
        # Reset code is valid
        return True
    else:
        # Reset code is invalid
        return False