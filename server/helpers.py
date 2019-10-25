'''
Helper functions
Checks user validity
Gets data
'''
import re
import server.global_var as global_var
import jwt
import hashlib

# Decodes a token
def decode_token(token):
    return jwt.decode(token, SECRET, algorithms=['HS256'])

# Encodes user id
def encode_token_for_u_id(u_id):
    return jwt.encode({"u_id": u_id}, SECRET, algorithm=['HS256'])

# Hashes a code
def hash(code):
    return hashlib.sha256(code.encode()).hexdigest()

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

    # Checking if token is an owner
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
    '''
    Checking if a name is valid
    '''
    if len(name) > 0 and len(name) <= 50:
        return True
    else:
        return False

def valid_user_id(u_id):
    '''
    Checking if a user_id is valid
    '''
    for user in global_var.data["users"]:
        if user.u_id == u_id:
            return True
    return False

def valid_token(token):
    '''
    Checks if a user token is valid
    '''
    for token in global_var.data["token"]:
        return True
    return False

def valid_permission_id(permission_id):
    """
    Checks if a permission is valid
    """
    if permission_id == 1:
        # Owner
        return True
    elif permission_id == 2:
        # Admin
        return True
    elif permission_id == 3:
        # User
        return True
    else:
        # Invalid permission_id
        return False

def get_user_by_u_id(u_id):
    """
    Returns user class according to their user identification
    """
    # Checking validity of u_id
    if not valid_user_id(u_id):
        raise ValueError("Invalid User ID")

    # Finding user object using u_id
    for user in global_var.data["users"]:
        if user.u_id == u_id:
            return user

def get_user_by_token(token):
    """
    Returns user object according to their token
    """
    # Checking validity of token
    if not valid_token(token):
        raise ValueError("Invalid token")

    # Decoding token
    u_id = jwt.decode(token, SECRET, algorithms=['HS256'])
    
    # Finding user_id
    for user in global_var.data["user"]:
        if user.u_id == u_id:
            return user

def get_user_token_by_u_id(u_id):
    """
    Returns user token according to their token
    """
    # Checking validity of u_id
    if not valid_user_id(u_id):
        raise ValueError("Invalid u_id")
    
    return encode_token_for_u_id(u_id)