'''
Authorisation functions abstracted from the HTTP routes
'''
import hashlib
import random
import jwt
from flask_mail import Message
import server.global_var as data
from server.helpers import get_user_by_email, valid_email, valid_name, \
     get_user_by_reset_code, remove_reset, add_reset


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

    token = get_token(user.u_id)
    data.data["tokens"].append(token)
    return {"u_id": user.u_id, "token": token}

def auth_logout(token):
    '''
    Given an active token, invalidates the taken to log the user out. Given a
    non-valid token, does nothing
    '''

    # Deleting token
    if token in data.data["tokens"]:
        data.data["tokens"].remove(token)
        return {"is_success": True}

    return {"is_success": False}


def auth_register(email, password, name_first, name_last):
    '''
    Given a user's first and last name, email address, and password, create a
    new account for them and return a new token for authentication in their
    session
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
    new_u_id = len(data.data["users"])
    token = get_token(new_u_id)

    user = data.User(new_u_id, email, hash_password(password), name_first, name_last)

    # Make the first user slackr owner
    if not data.data["users"]:
        user.change_permissions(1)

    data.data["users"].append(user)

    data.data["tokens"].append(token)

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

    # Creating mail to send
    msg = Message("Website Reset Request",
                  sender="comp1531shared@gmail.com",
                  recipients=[email])
    msg.body = f"Your reset code is: {reset_code}"

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
    ''' Checks if a password is a valid password to be registered'''
    return len(password) >= 6

def get_token(u_id):
    ''' Encodes a user id to create a token '''
    return jwt.encode({"u_id": u_id}, data.SECRET, algorithm='HS256').decode("utf-8")

def hash_password(password):
    ''' Creates a hashed password to store '''
    return hashlib.sha256(password.encode()).hexdigest()


def generate_reset_code(user):
    ''' Generate reset code '''
    reset_code = hashlib.sha256(str(random.random()).encode()).hexdigest()
    # Access and place reset code into data
    add_reset(reset_code, user)

    return reset_code
