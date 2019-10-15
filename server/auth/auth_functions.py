from global_var import data
import re 

# Given a registered user's email and password and generates a valid token
# for the user to remain authenticated
def auth_login(email, password):
    if valid_email(email) == False:
        raise ValueError("Invalid Email")
    if registered_email(email) == False:
        raise ValueError("Email not registered")
    if registered_account(email, password) == False:
        raise ValueError("Password Incorrect")

    return {"u_id": "valid_u_id", "token": "valid_token"}

# Given an active token, invalidates the taken to log the user out. Given a 
# non-valid token, does nothing
def auth_logout(token):
    if valid_token(token) == True:
        # Remove token from server
        pass

    return {}

# Given a user's first and last name, email address, and password, create a new 
# account for them and return a new token for authentication in their session
def auth_register(email, password, name_first, name_last):
    if valid_email(email) == False:
        raise ValueError("Invalid Email")
    if registered_email(email) == True:
        raise ValueError("Email Already Registered")
    if valid_password(password) == False:
        raise ValueError("Password Not Strong")
    if valid_name_first(name_first) == False:
        raise ValueError("Invalid First Name")
    if valid_name_last(name_last) == False:
        raise ValueError("Invalid Last Name")

    data["users"].append({"u_id":len(data["users"]), \
                            "password": password, "email": email, \
                            "name_first": name_first,"name_last": name_last, \
                            "handle": create_handle(name_first,name_last)})

    return {"u_id": "valid_u_id", "token": "valid_token"}

"""
Given an email address, if the user is a registered user, send's them a an 
email containing a specific secret code, that when entered in 
auth_passwordreset_reset, shows that the user trying to reset the password 
is the one who got sent this email.
"""
def auth_passwordreset_request(email):
    # Send password to associated email

    return {}

# Given a reset code for a user, set that user's new password to the password 
# provided
def auth_passwordreset_reset(reset_code, new_password):
    if valid_reset_code(reset_code) == False:
        raise ValueError("Invalid Reset Code")
    if valid_password(new_password) == False:
        raise ValueError("Invalid Password")

    return {}


# Helper Functions
# Checks if an email is a valid email to be registered
def valid_email(email):  
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(regex,email)):  
        return True       
    else:  
        return False

# Checks if a password is a valid password to be registered
def valid_password(password):
    if len(password) > 6 and len(password) < 30:
        return True
    else:
        return False

# Checks if first name is valid to be registered
def valid_name_first(name_first):
    if len(name_first) > 1 and len(name_first) < 50:
        return True
    else:
        return False

# Checks if last name is valid to be registered
def valid_name_last(name_last):
    if len(name_last) > 1 and len(name_last) < 50:
        return True
    else:
        return False

#Creates a handle for a newly registere user
def create_handle(name_first, name_last):
    return "handle"

# Checks if an email is a registered user to log in
def registered_email(email):
    
    #Loops through users to find matching email
    for users in data["users"]:
        if email in users:
            return True
        
    return False

# Checks if a user email and password are matched to log in
def registered_account(email, password):

    #Loops through users to find matching email
    for users in data["users"]:
        if email in users:
            if password in users:
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