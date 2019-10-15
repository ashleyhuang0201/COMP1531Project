
from server.helper.Error import AccessError
#from server.global_var import data
import re 
import jwt

SECRET = "token_hash"


# Given a registered user's email and password and generates a valid token
# for the user to remain authenticated
def auth_login(email, password):
    if valid_email(email) == False:
        raise ValueError("Invalid Email")
    if registered_email(email) == False:
        raise ValueError("Email not registered")
    if registered_account(email, password) == False:
        raise ValueError("Password Incorrect")

    for user in data["users"]:
        if user["email"] == email:
            data["tokens"].append(get_token(user["u_id"]))
            return {"u_id": user["u_id"], "token": get_token(user["u_id"])}
        

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
    if valid_name(name_first) == False:
        raise ValueError("Invalid First Name")
    if valid_name(name_last) == False:
        raise ValueError("Invalid Last Name")

    new_u_id = len(data["users"])
    token = get_token(new_u_id)

    data["users"].append({"u_id": new_u_id, \
                            "password": password, "email": email, \
                            "name_first": name_first,"name_last": name_last, \
                            "handle": create_handle(name_first,name_last)})

    return {"u_id": new_u_id, "token": token}

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


""" Helper Functions"""

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

# Checks if a name is valid to be registered
def valid_name(name):
    if len(name) > 1 and len(name) < 50:
        return True
    else:
        return False

#Creates a handle for a newly registere user
def create_handle(name_first, name_last):
    return "handle"

# Checks if an email is already a registered email
def registered_email(email):
    
    #Loops through users to find matching email
    for user in data["users"]:
        if user["email"] == email:
            return True
        
    return False

# Checks if a user email and password are matched to log in
def registered_account(email, password):

    #Loops through users to find matching email
    for user in data["users"]:
        if user["email"] == email:
            if user["password"] == password:
                return True
            else:
                return False

def get_token(u_id):
    return jwt.encode({'some': 'payload'}, SECRET, algorithm='HS256')

# Checks the activeness of a token
def valid_token(token):
    if token in data["tokens"]:
        return True
    else:
        return False

# Checks if a reset code is valid
def valid_reset_code(reset_code):
    if reset_code == "valid_reset_code":
        return True
    else:
        return False