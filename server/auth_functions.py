'''
Authorisation functions abstracted from the HTTP routes
'''
import hashlib
import jwt
import random
from flask import Flask
from flask_mail import Mail, Message
from json import dumps

import server.global_var as data
import server.helpers as helper


def auth_login(email, password):
    '''
    Given a registered user's email and password function generates and returns a 
    user_id and token assigned to the account
    '''
    user = helper.get_user_by_email(email)
    # Check validity of login
    if not helper.valid_email(email):
        raise ValueError("Invalid Email")
    if not user:
        raise ValueError("Email not registered")
    
    if not user.password == hashPassword(password):
        raise ValueError("Password Incorrect")

    token = get_token(user.u_id)
    data.data["tokens"].append(token)
    return {"u_id": user["u_id"], "token": token}


# Given an active token, invalidates the taken to log the user out. Given a
# non-valid token, does nothing
def auth_logout(token):
    # Deleting token
    if token in data.data["tokens"]:
        data.data["tokens"].remove(token)

    return {}

# Given a user's first and last name, email address, and password, create a new
# account for them and return a new token for authentication in their session
def auth_register(email, password, name_first, name_last):
    # Checking if registration details are valid
    user = helper.get_user_by_email(email)

    if not helper.valid_email(email):
        raise ValueError("Invalid Email")
    if user:
        raise ValueError("Email Already Registered")
    if not valid_password(password):
        raise ValueError("Password Not Strong")
    if not helper.valid_name(name_first):
        raise ValueError("Invalid First Name")
    if not helper.valid_name(name_last):
        raise ValueError("Invalid Last Name")

    # Adding new user details
    new_u_id = len(data.data["users"])
    token = get_token(new_u_id)

    user = data.User(new_u_id, email, hashPassword(password), name_first, name_last)

    # Make the first user slackr owner
    if len(data.data["users"]) == 0:
        user.change_permissions(1)

    data.data["users"].append(user)

    data.data["tokens"].append(token)

    return { "u_id": new_u_id, "token": token}

def auth_passwordreset_request(email):
    '''
    Given an email address, if the user is a registered user, send's them a an
    email containing a specific secret code, that when entered in
    auth_passwordreset_reset, shows that the user trying to reset the password
    is the one who got sent this email.
    '''
    if helper.valid_email(email) == False:
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
    user = helper.get_user_by_email(email)
    reset_code = generate_reset_code(user)

    # Creating mail to send
    mail = Mail(APP)
    msg = Message("Website Reset Request",
        sender="comp1531shared@gmail.com",
        recipients=[email])
    msg.body = f"Your reset code is: {reset_code}"
    mail.send(msg)

    return {}

def auth_passwordreset_reset(reset_code, new_password):
    '''
    Given a reset code for a user, set that user's new password to the password
    provided
    '''

    user = helper.get_user_by_reset_code(reset_code)

    if not user:
        raise ValueError("Invalid Reset Code")
    if not valid_password(new_password):
        raise ValueError("Invalid Password")

    user.change_password(new_password)
    helper.remove_reset(reset_code)

    return {}


# Helper Functions specific to auth

def valid_password(password):
    ''' Checks if a password is a valid password to be registered''' 
    if len(password) >= 6:
        return True
    else:
        return False

def get_token(u_id):
    return jwt.encode({"u_id": u_id}, data.SECRET, algorithm='HS256').decode("utf-8")

# Creates a hashed password to store
def hashPassword(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Generate reset code
def generate_reset_code(user):
    reset_code = hashlib.sha256(str(random.random()).encode()).hexdigest()
    # Access and place reset code into data
    helper.add_reset(reset_code, user)

    return reset_code