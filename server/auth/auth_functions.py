'''
Authorisation functions abstracted from the HTTP routes
'''

import hashlib
import jwt

import server.global_var as global_var
from server.helper.valid_checks import valid_email, valid_name

SECRET = "token_hash"

def auth_login(email, password):
    '''
    Given a registered user's email and password and generates a valid token
    for the user to remain authenticated
    '''
    if not valid_email(email):
        raise ValueError("Invalid Email")
    if not registered_email(email):
        raise ValueError("Email not registered")
    if not registered_account(email, password):
        raise ValueError("Password Incorrect")

    for user in global_var.data["users"]:
        if user["email"] == email:
            global_var.data["tokens"].append(get_token(user["u_id"]))
            return {"u_id": user["u_id"], "token": str(get_token(user["u_id"]))}


# Given an active token, invalidates the taken to log the user out. Given a
# non-valid token, does nothing
def auth_logout(token):
    if token in global_var.data["tokens"]:
        global_var.data["tokens"].remove(token)

    return {}

# Given a user's first and last name, email address, and password, create a new
# account for them and return a new token for authentication in their session
def auth_register(email, password, name_first, name_last):

    if not valid_email(email):
        raise ValueError("Invalid Email")
    if registered_email(email):
        raise ValueError("Email Already Registered")
    if not valid_password(password):
        raise ValueError("Password Not Strong")
    if not valid_name(name_first):
        raise ValueError("Invalid First Name")
    if not valid_name(name_last):
        raise ValueError("Invalid Last Name")

    new_u_id = len(global_var.data["users"])
    token = get_token(new_u_id)

    global_var.data["users"].append({"u_id": new_u_id, \
                            "password": password, "email": email, \
                            "name_first": name_first, "name_last": name_last, \
                            "handle": create_handle(name_first, name_last)})

    global_var.data["tokens"].append(str(token))

    return { "u_id": new_u_id, "token": str(token)}

def auth_passwordreset_request(email):
    '''
    Given an email address, if the user is a registered user, send's them a an
    email containing a specific secret code, that when entered in
    auth_passwordreset_reset, shows that the user trying to reset the password
    is the one who got sent this email.
    '''

    return {}

def auth_passwordreset_reset(reset_code, new_password):
    '''
    Given a reset code for a user, set that user's new password to the password
    provided
    '''
    if not valid_reset_code(reset_code):
        raise ValueError("Invalid Reset Code")
    if not valid_password(new_password):
        raise ValueError("Invalid Password")

    return {}


# Helper Functions specific to auth

def valid_password(password):
    ''' Checks if a password is a valid password to be registered''' 
    if len(password) >= 6:
        return True
    else:
        return False

def create_handle(name_first, name_last):
    ''' Creates a handle for a newly registered user '''
    return str(f"{name_first}{name_last}")

# Checks if an email is already a registered email
def registered_email(email):

    #Loops through users to find matching email
    for user in global_var.data["users"]:
        if user["email"] == email:
            return True

    return False

# Checks if a user email and password are matched to log in
def registered_account(email, password):

    #Loops through users to find matching email
    for user in global_var.data["users"]:
        if user["email"] == email:
            if user["password"] == password:
                return True
            else:
                return False


def get_token(u_id):
    global SECRET
    return jwt.encode({"u_id": u_id}, SECRET, algorithm='HS256')

def get_user(token):
    global SECRET
    return jwt.decode(token, SECRET, algorithms=['HS256'])

# Creates a hashed password to store
def hashPassword(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Checks the activeness of a token
def valid_token(token):
    if token in global_var.data["tokens"]:
        return True
    else:
        return False

# Checks if a reset code is valid
def valid_reset_code(reset_code):
    if reset_code == "valid_reset_code":
        return True
    else:
        return False