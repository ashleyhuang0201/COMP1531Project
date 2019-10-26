'''
Helper functions
Checks user validity
Gets data
'''
import re
import jwt
import hashlib
import server.global_var as data
from server.Error import AccessError

# Decodes a token
def decode_token(token):
    return jwt.decode(token, data.SECRET, algorithms=['HS256'])["u_id"]

# Encodes user id
def encode_token_for_u_id(u_id):
    return jwt.encode({
        "u_id": u_id
        }, data.SECRET, algorithm='HS256').decode("utf-8")


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
    for user in data.data["users"]:
        if user.u_id == u_id:
            return True
    return False

def valid_token(token):
    '''
    Checks if a user token is valid
    '''
    for tok in data.data["tokens"]:
        if tok == token:
            return True
    return False

def valid_permission_id(permission_id):
    """
    Checks if a permission is valid
    """
    if permission_id < 1 or permission_id > 3:
        return False
    return True

def get_user_by_u_id(u_id):
    """
    Returns user class according to their user identification
    """
    # Checking validity of u_id
    if not valid_user_id(u_id):
        raise ValueError("Invalid User ID")

    # Finding user object using u_id
    for user in data.data["users"]:
        if user.u_id == u_id:
            return user

def get_user_by_token(token):
    """
    Returns user object according to their token
    """
    # Checking validity of token
    if not valid_token(token):
        raise AccessError("Invalid token")

    # Decoding token
    u_id = jwt.decode(token, data.SECRET, algorithms=['HS256'])["u_id"]
    
    # Finding user_id
    for user in data.data["users"]:
        if user.u_id == u_id:
            return user
    return None

def get_user_token_by_u_id(u_id):
    """
    Returns user token according to their token
    """
    # Checking validity of u_id
    if not valid_user_id(u_id):
        raise ValueError("Invalid u_id")
    
    return encode_token_for_u_id(u_id)

def get_channel_by_channel_id(id):
    for channel in data.data["channels"]:
        if channel.id == id:
            return channel
    return 

def get_user_by_reset_code(reset_code):
    for entry in data.data["reset_code"]:
        if entry["reset_code"] == reset_code:
            return entry["users"]
    raise ValueError("Invalid reset code")
    
def get_user_by_email(email):
    for user in data.data["users"]:
        if user.email == email:
            return user
    return None

def remove_reset(code):
    for entry in data.data["reset_code"]:
        if entry["reset_code"] == code:
            data.data["reset_code"].remove(entry)

def add_reset(code, email):
    user = get_user_by_email(email)
    data.data["reset_code"].append({"reset_code": code, "user": user})

# Returns the channel object corresponding to the channel_id
def get_channel_by_channel_id(channel_id):
    for channel in data.data["channels"]:
        if channel_id == channel.id:
            return channel

# Returns the channel object according to the message_id
def get_channel_by_message_id(message_id):
    for channel in data.data["channels"]:
        for message in channel.messages:
            if message.id == message_id:
                return channel

# Returns the message object corresponding to message id
def get_message_by_message_id(message_id):
    for channel in data.data["channels"]:
        for message in channel.messages:
            if message.id == message_id:
                return message
