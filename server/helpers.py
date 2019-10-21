'''
Helper functions that check validity of user data
'''
import re
import server.global_var as global_var

def token_is_admin(token):
    """
    Checks if a token is related to an admin
    """
    # Checking validity of token
    if not valid_token(token):
        raise ValueError("Invalid token")

    # Checking if token is an admin
    user = get_user_by_token(token)
    if user.permission == 2:
        return True
    else:
        return False

def token_is_owner(token):
    """
    Checks if a token is related to an owner
    """
    # Checking validity of token
    if not valid_token(token):
        raise ValueError("Invalid token")

    # Checking if token is an admin
    user = get_user_by_token(token)
    if user.permission == 1:
        return True
    else:
        return False

def valid_email(email):
    ''' Checks if an email is a valid email '''
    # r prefix treats as raw string - works without but pytest and pylint don't
    # like it
    regex = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    if re.search(regex, email):
        return True
    else:
        return False

def valid_name(name):
    ''' Checks if a name is valid to be registered '''
    if len(name) >= 1 and len(name) <= 50:
        return True
    else:
        return False

def valid_user_id(u_id):
    ''' Checks if a user_id is valid '''
    if u_id == "valid_u_id":
        return True
    return False

def valid_token(token):
    ''' Checks if a user_id is valid '''
    if token == "valid_token":
        return True
    return False

def valid_permission_id(permission_id):
    if permission_id == 1:
        return True
    elif permission_id == 2:
        return True
    elif permission_id == 3:
        return True
    else:
        return False

def get_user_by_u_id(u_id):
    """
    Returns user class according to their user identification
    """
    # Checking validity of u_id
    if not valid_user_id(u_id):
        raise ValueError("Invalid User ID")

    for user in global_var.data["users"]:
        if user.u_id == u_id:
            return user

def get_user_by_token(token):
    """
    Returns user class according to their token
    """
    # Checking validity of token
    if not valid_token(token):
        raise ValueError("Invalid token")

    # Finding user_id from token
    # To do
    # Reverse token
    """
    for user in global_var.data["users"]:
        if user.u_id == u_id:
            return user
    """