'''
Helper functions
Checks user validity
Gets data
'''
import re
import jwt
import server.global_var as data
from server.Error import AccessError

# Decodes a token
def decode_token(token):
    """
    Decodes a token using jwt
    """
    return jwt.decode(token, data.SECRET, algorithms=['HS256'])["u_id"]

# Encodes user id
def encode_token_for_u_id(u_id):
    """
    Encodes a token using jwt
    """
    return jwt.encode({
        "u_id": u_id
        }, data.SECRET, algorithm='HS256').decode("utf-8")

# Checks if a token is an admin
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
    return False

# Checks if a token is an owner
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
    return False

# Checks if an email is valid
def valid_email(email):
    '''
    Checks if an email is a valid email
    '''
    regex = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    if re.search(regex, str(email)):
        return True
    return False

# Checks if a name is valid
def valid_name(name):
    '''
    Checking if a name is valid (1 character to 50 characters)
    '''
    if len(name) > 0 and len(name) <= 50:
        return True
    return False

# Checks if a user_id is valid
def valid_user_id(u_id):
    '''
    Checking if a user_id is valid
    '''
    for user in data.data["users"]:
        if user.u_id == u_id:
            return True
    return False

# Checks if a token is valid
def valid_token(token):
    '''
    Checks if a user token is valid
    '''
    for tok in data.data["tokens"]:
        if tok == token:
            return True
    return False

# Checks if a permission_id is valid
def valid_permission_id(permission_id):
    """
    Checks if a permission is valid
    """
    if permission_id < 1 or permission_id > 3:
        return False
    return True

# Obtain user object using u_id
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
    return None

# Obtain user object using a token
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

# Obtains user token using user id
def get_user_token_by_u_id(u_id):
    """
    Returns user token according to their token
    """
    # Checking validity of u_id
    if not valid_user_id(u_id):
        raise ValueError("Invalid u_id to find token")

    return encode_token_for_u_id(u_id)

# Finds u_id according to reset code
def get_user_by_reset_code(reset_code):
    """
    Returns u_id from users who currently have an active reset_code
    """
    for entry in data.data["reset_code"]:
        if entry["reset_code"] == reset_code:
            return entry["user"]
    return None

# Finds user object according to email
def get_user_by_email(email):
    """
    Returns user object from users who have a registered email
    """
    for user in data.data["users"]:
        if user.email == email:
            return user
    return None

# Deleting reset_code
def remove_reset(code):
    """
    Turns a valid reset code to an invalid reset code
    """
    code_deleted = False
    for entry in data.data["reset_code"]:
        if entry["reset_code"] == code:
            code_deleted = True
            data.data["reset_code"].remove(entry)
    if code_deleted is False:
        raise ValueError("No code was deleted")

# Add reset_code
def add_reset(code, user):
    """
    Adds a new reset code
    """
    data.data["reset_code"].append({"reset_code": code, "user": user})

# Returns the channel object corresponding to the channel_id
def get_channel_by_channel_id(channel_id):
    """
    Returns channel object which has the channel_id
    """
    for channel in data.data["channels"]:
        if channel_id == channel.id:
            return channel
    return None

# Returns the channel object according to the message_id
def get_channel_by_message_id(message_id):
    """
    Returns a channel object where it contains a message with message_id
    """
    for channel in data.data["channels"]:
        for message in channel.messages:
            if message.id == message_id:
                return channel
    return None

# Returns the message object corresponding to message id
def get_message_by_message_id(message_id):
    """
    Returns a message object where the message has message_id
    """
    for channel in data.data["channels"]:
        for message in channel.messages:
            if message.id == message_id:
                return message
    return None

# Return a reset code from a user email
def get_reset_code_from_email(email):
    """
    Returns a reset_code according to a user email
    """
    for entry in data.data["reset_code"]:
        if entry["user"].email == email:
            return entry["reset_code"]
    return None
