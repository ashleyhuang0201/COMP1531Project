'''
Team: You_Things_Can_Choose
Authorisation functions abstracted from the HTTP routes
'''

import hashlib
import random
from flask_mail import Message
from flask import request
import server.global_var as data
from server.constants import MINIMUM_PASSWORD_LENGTH, SLACKR_OWNER
from server.Error import ValueError
from server.helpers import (activate_token, add_reset, add_user,
                            deactive_token, encode_token_for_u_id,
                            get_new_u_id, get_user_by_email,
                            get_user_by_reset_code, remove_reset, valid_email,
                            valid_name)

def auth_login(email, password):
    '''
    Given a registered user's email and password function generates and
    returns a user_id and token assigned to the account
    '''

    user = get_user_by_email(email)

    # Check validity of login
    if not valid_email(email):
        raise ValueError("Invalid Email")
    if not user:
        raise ValueError("Email not registered")
    if not user.password == hash_password(password):
        raise ValueError("Password Incorrect")

    token = encode_token_for_u_id(user.u_id)

    # Sets token as an active token
    activate_token(token)

    return {"u_id": user.u_id, "token": token}

def auth_logout(token):
    '''
    Given an active token, invalidates the taken to log the user out. Given a
    non-valid token, does nothing
    '''

    # Deletes a token
    if deactive_token(token):
        return {"is_success": True}

    return {"is_success": False}

def auth_register(email, password, name_first, name_last):
    '''
    Given a user's first and last name, email address, and password, create a
    new account for them and return a new token for authentication in their
    session. A handle is generated that is the concatentation of a
    lowercase-only first name and last name. If the concatenation is longer
    than 20 characters, it is cutoff at 20 characters. If the handle is already
    taken, you may modify the handle in any way you see fit to make it unique.
    '''

    # Checking if registration details are valid
    user = get_user_by_email(email)

    if not valid_email(email):
        raise ValueError("Invalid Email")
    if user:
        raise ValueError("Email Already Registered")
    if not valid_password(password):
        raise ValueError("Password Not Strong")
    if not valid_name(name_first):
        raise ValueError("Invalid First Name")
    if not valid_name(name_last):
        raise ValueError("Invalid Last Name")

    # Adding new user details
    new_u_id = get_new_u_id()
    token = encode_token_for_u_id(new_u_id)

    user = data.User(new_u_id, email, hash_password(password), \
         name_first, name_last)

    # Make the first user slackr owner
    if new_u_id == 0:
        user.change_permissions(SLACKR_OWNER)

    # Appends user to data
    add_user(user)

    # Sets token as active (user is logged in)
    activate_token(token)

    return {"u_id": new_u_id, "token": token}

def auth_passwordreset_request(email):
    '''
    Given an email address, if the user is a registered user, send's them an
    email containing a specific secret code, that when entered in
    auth_passwordreset_reset, shows that the user trying to reset the password
    is the one who got sent this email.
    '''

    if not valid_email(email):
        raise ValueError("Email is not valid")

    # Preparing reset code
    user = get_user_by_email(email)
    reset_code = generate_reset_code(user)
    try:
        redirect_url = f"{request.headers['Origin']}/reset_password"
    except:
        redirect_url = "http://127.0.0.1:8001/reset_password"

    # Creating mail to send
    msg = Message("Website Reset Request",
                  sender="comp1531shared@gmail.com",
                  recipients=[email])
    msg.html = ("<p>Your reset code is:</p>"
                f"<p>\n<b>{reset_code}</b>\n</p>"
                f"<p>Copy this code into the field at {redirect_url}</p>")

    # Empty dictionary is manually returned in server.py
    return msg

def auth_passwordreset_reset(reset_code, new_password):
    '''
    Given a reset code for a user, set that user's new password to the password
    provided
    '''

    user = get_user_by_reset_code(reset_code)

    if not valid_password(new_password):
        raise ValueError("Invalid Password")
    if not user:
        raise ValueError("Invalid Reset Code")

    user.change_password(new_password)
    remove_reset(reset_code)

    return {}

# Helper Functions specific to auth

def valid_password(password):
    '''
    Checks if a password is a valid password to be registere
    '''

    return len(password) >= MINIMUM_PASSWORD_LENGTH

def hash_password(password):
    '''
    Creates a hashed password to store
    '''

    return hashlib.sha256(password.encode()).hexdigest()

def generate_reset_code(user):
    '''
    Generate reset code
    '''

    reset_code = str(hashlib.sha256(str(random.random()).encode()).hexdigest())

    # Access and place reset code into data
    add_reset(reset_code, user)

    return reset_code
