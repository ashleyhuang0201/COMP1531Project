'''
Authorisation functions abstracted from the HTTP routes
'''
import hashlib
import jwt
import random
from flask import Flask
from flask_mail import Mail, Message
from json import dumps

import server.global_var as global_var
from server.helpers import valid_email, valid_name

SECRET = "9c055b2cc7394df69438fe14bc31cbe142898b1d8548360d2b4cddd990e97c69"

def auth_login(email, password):
    '''
    Given a registered user's email and password function generates and returns a 
    user_id and token assigned to the account
    '''
    # Check validity of login
    if not valid_email(email):
        raise ValueError("Invalid Email")
    if not registered_email(email):
        raise ValueError("Email not registered")
    if not registered_account(email, password):
        raise ValueError("Password Incorrect")

    # Logging in
    for user in global_var.data["users"]:
        if user.email == email:
            token = get_token(user.u_id)
            global_var.data["tokens"].append(token)
            return {"u_id": user["u_id"], "token": str(get_token(user["u_id"]))}


# Given an active token, invalidates the taken to log the user out. Given a
# non-valid token, does nothing
def auth_logout(token):
    # Deleting token
    if token in global_var.data["tokens"]:
        global_var.data["tokens"].remove(token)

    return {}

# Given a user's first and last name, email address, and password, create a new
# account for them and return a new token for authentication in their session
def auth_register(email, password, name_first, name_last):
    # Checking if registration details are valid
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

    # Adding new user details
    new_u_id = len(global_var.data["users"])
    token = get_token(new_u_id)

    user = global_var.User(new_u_id, email, hashPassword(password), name_first, name_last)

    global_var.data["users"].append(user)

    global_var.data["tokens"].append(str(token))

    return { "u_id": new_u_id, "token": str(token)}

def auth_passwordreset_request(email):
    '''
    Given an email address, if the user is a registered user, send's them a an
    email containing a specific secret code, that when entered in
    auth_passwordreset_reset, shows that the user trying to reset the password
    is the one who got sent this email.
    '''
    if valid_email(email) == False:
        raise ValueError("Email is not valid")

    # Creating email server
    APP = Flask(__name__)
    APP.config.update(
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USERNAME = "comp1531shared@gmail.com",
        MAIL_PASSWORD = "ThanksGuys"
    )

    # Preparing reset code
    reset_code = generate_reset_code()
    user = find_user_by_email(email)
    user.add_reset_code(reset_code)

    # Creating mail to send
    mail = Mail(APP)
    msg = Message("Website Reset Request",
        sender="comp1531shared@gmail.com",
        recipients=[email])
    msg.body = "Your reset code is: " + reset_code
    mail.send(msg)

    return dumps({})

def auth_passwordreset_reset(reset_code, new_password):
    '''
    Given a reset code for a user, set that user's new password to the password
    provided
    '''
    if not valid_reset_code(reset_code):
        raise ValueError("Invalid Reset Code")
    if not valid_password(new_password):
        raise ValueError("Invalid Password")

    user = find_user_by_reset_code(reset_code)
    user.change_password(new_password)

    return dumps({})


# Helper Functions specific to auth

def valid_password(password):
    ''' Checks if a password is a valid password to be registered''' 
    if len(password) >= 6:
        return True
    else:
        return False

# Checks if an email is already a registered email
def registered_email(email):

    #Loops through users to find matching email
    for user in global_var.data["users"]:
        if user.email == email:
            return True

    return False

# Checks if a user email and password are matched to log in
def registered_account(email, password):

    #Loops through users to find matching email
    for user in global_var.data["users"]:
        if user.email == email:
            if user.password == password:
                return True
            else:
                return False


def get_token(u_id):
    global SECRET
    return jwt.encode({"u_id": u_id}, SECRET, algorithm='HS256')

def get_id(token):
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

# Generate reset code
def generate_reset_code():
    reset_code = random.random()
    # Access and place reset code into data - Todo

    return reset_code