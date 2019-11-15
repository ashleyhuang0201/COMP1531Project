'''
Helper functions
Checks user validity
Gets data
'''
import re
import jwt
import datetime as dt
from hashlib import sha256

from server import global_var as data
from server.Error import AccessError, ValueError

#Constants
MIN_NAME_LENGTH = 1
MAX_NAME_LENGTH = 50
MAX_HANDLE_LENGTH = 20
SLACKER_OWNER = 1
SLACKER_ADMIN = 2
SLACKR_USER = 3

def valid_token(function):
    ''' Decorator for checking if a token is valid '''
    def wrapper(*args, **kwargs):
        token = list(args)[0]
        for active_token in data.data["tokens"]:
            if active_token == token:
                return function(*args, **kwargs)
        raise AccessError("Invalid token")
    return wrapper

def decode_token(token):
    ''' Decodes a token using jwt '''
    return jwt.decode(token, data.SECRET, algorithms=['HS256'])["u_id"]

def encode_token_for_u_id(u_id):
    ''' Encodes a token using jwt '''
    return jwt.encode({
        "u_id": u_id
        }, data.SECRET, algorithm='HS256').decode("utf-8")

@valid_token
def token_is_admin(token):
    ''' Checks if a token is  an admin '''
    user = get_user_by_token(token)
    if user.permission == SLACKER_ADMIN:
        return True
    return False

@valid_token
def token_is_owner(token):
    ''' Checks if a token is  an owner '''
    user = get_user_by_token(token)
    if user.permission == SLACKER_OWNER:
        return True
    return False

def valid_email(email):
    ''' Checks if an email is a valid email '''
    regex = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    if re.search(regex, str(email)):
        return True
    return False

def valid_name(name):
    ''' Checking if a name is of valid length '''
    if len(name) >= MIN_NAME_LENGTH and len(name) <= MAX_NAME_LENGTH:
        return True
    return False

def valid_user_id(u_id):
    ''' Checking if a user_id is valid '''
    for user in data.data["users"]:
        if user.u_id == u_id:
            return True
    return False

def valid_permission_id(permission_id):
    ''' Checks if a permission is valid '''
    if permission_id < SLACKER_OWNER or permission_id > SLACKR_USER:
        return False
    return True

def get_user_by_u_id(u_id):
    ''' Returns user class according to their user identification '''
    # Checking validity of u_id
    if not valid_user_id(u_id):
        raise ValueError("Invalid User ID")

    # Finding user object using u_id
    for user in data.data["users"]:
        if user.u_id == u_id:
            return user
    return None

@valid_token
def get_user_by_token(token):
    ''' Returns user object according to their token '''

    # Decoding token
    u_id = decode_token(token)

    # Finding user corresponding to user_id
    for user in data.data["users"]:
        if user.u_id == u_id:
            return user
    return None


def get_user_token_by_u_id(u_id):
    ''' Returns user token according to their token '''

    # Checking validity of u_id
    if not valid_user_id(u_id):
        raise ValueError("Invalid u_id to find token")

    return encode_token_for_u_id(u_id)

def get_user_by_reset_code(reset_code):
    ''' Returns u_id from users who currently have an active reset_code '''
    for entry in data.data["reset_code"]:
        if entry["reset_code"] == reset_code:
            return entry["user"]
    return None

def get_user_by_email(email):
    ''' Returns user object from users who have a registered email '''
    for user in data.data["users"]:
        if user.email == email:
            return user
    return None

def remove_reset(code):
    ''' Turns a valid reset code to an invalid reset code '''
    code_deleted = False
    for entry in data.data["reset_code"]:
        if entry["reset_code"] == code:
            code_deleted = True
            data.data["reset_code"].remove(entry)
    if code_deleted is False:
        raise ValueError("No code was deleted")

def add_reset(code, user):
    ''' Adds a new reset code '''

    data.data["reset_code"].append({"reset_code": code, "user": user})

def get_channel_by_channel_id(channel_id):
    ''' Returns channel object which has the channel_id '''
    for channel in data.data["channels"]:
        if channel_id == channel.id:
            return channel
    return None

def get_channel_by_message_id(message_id):
    '''
    Returns a channel object where it contains a message with message_id
    '''
    for channel in data.data["channels"]:
        for message in channel.messages:
            if message.id == message_id:
                return channel
    return None

def get_message_by_message_id(message_id):
    ''' Returns a message object where the message has message_id '''
    for channel in data.data["channels"]:
        for message in channel.messages:
            if message.id == message_id:
                return message
    return None

def get_reset_code_from_email(email):
    ''' Returns a reset_code according to a user email '''
    for entry in data.data["reset_code"]:
        if entry["user"].email == email:
            return entry["reset_code"]
    return None

def valid_crop(x_start, x_end, y_start, y_end, width, height):
    '''
    Checking if the crop coordinates are within the bounds of the image
    '''
    # Checking validity of x_start (x_start cannot be before the first
    # pixel nor be the ending pixel)
    if x_start < 0 or x_start >= width:
        raise ValueError("x_start is invalid")

    # Checking validity of x_end (x_end cannot be the first pixel or after
    # the final pixel)
    if x_end <= 0 or x_end > width:
        raise ValueError("x_end is invalid")

    # Checking validity of y_start (y_start cannot be before the first pixel
    # nor be the ending pixel)
    if y_start < 0 or y_start >= height:
        raise ValueError("y_start is invalid")

    # Checking validity of y_end (y_end cannot be the first pixel nor
    # after the final pixel)
    if y_end <= 0 or y_end > height:
        raise ValueError("y_end is invalid")

    # Checking if the image is at least a pixel size
    if x_start == x_end:
        raise ValueError("An image of no pixels is not an image")
    if y_start == y_end:
        raise ValueError("An image of no pixels is not an image")

def generate_handle(name_first, name_last, u_id):
    """
    A handle is generated that is the concatentation of a lowercase-only first
    name and last name. If the concatenation is longer than 20 characters, it
    is cutoff at 20 characters. If the handle is already taken, you may modify
    the handle in any way you see fit to make it unique.
    """
    # A handle is the concatentation of lower-case first_name and last_name
    handle = str(name_first.lower()) + str(name_last.lower())

    # If the concatenation is longer than 20 characters, it is cutoff at 20
    handle = handle[:MAX_HANDLE_LENGTH]

    # Checking if unique handle
    if unique_handle(handle):
        # Unique handle, can use
        return handle
    # Not unique handle
    # Trying to use the requested handle
    handle = str(u_id) + handle
    handle = handle[:MAX_HANDLE_LENGTH]
    if not unique_handle(handle):
        # Further processing is required - using a number as the handle
        for i in range(10 ** MAX_HANDLE_LENGTH - 1):
            if unique_handle(str(i)):
                handle = str(i)
                break
    return handle

def unique_handle(handle):
    ''' Checks if a handle is unique '''
    for user in data.data["users"]:
        if user.handle == handle:
            return False
    return True

def create_photo_path(user):
    to_hash = f"{user.email}{user.password}{dt.datetime.now().timestamp()}"
    return(sha256(f"{to_hash}".encode()).hexdigest())
