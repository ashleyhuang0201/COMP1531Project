'''
Message functions Iteration 2 implementations
Team: You_Things_Can_Choose
'''
import datetime
from threading import Timer

import server.global_var as global_var
from server.constants import HEART_REACT, LIKE_REACT, MAX_MESSAGE_LENGTH
from server.Error import AccessError, ValueError
from server.helpers import (get_channel_by_channel_id,
                            get_channel_by_message_id,
                            get_message_by_message_id, get_user_by_token,
                            token_is_admin, token_is_owner, valid_token)


@valid_token
def message_sendlater(token, channel_id, message, time_sent):
    '''
    Sends a message from authorised_user to the channel specified by
    channel_id automatically at a specified time in the future
    '''

    channel = get_channel_by_channel_id(channel_id)
    user = get_user_by_token(token)

    # Channel_id does not refer to a valid channel
    if channel is None:
        raise ValueError("Invalid Channel ID")

    # Message is not of appropriate length
    if valid_message(message):
        raise ValueError("Message length too long")

    # Time to be sent is in the past
    if time_sent < datetime.datetime.now().timestamp():
        raise ValueError("Time sent was in the past")

    # User has not joined the channel
    if not channel.is_member(user.u_id):
        raise AccessError("Authorised user is not a member of the channel")

    # create new message object and update send time
    message_object = global_var.Message(user.u_id, message, channel_id)
    message_object.time_created = time_sent

    time_diff = time_sent - datetime.datetime.now().timestamp()
    Timer(time_diff, channel.add_message, args=[message_object]).start()

    return {
        "message_id": message_object.id
    }

@valid_token
def message_send(token, channel_id, message):
    '''
    Send a message from authorised_user to the channel specified by channel_id
    '''

    channel = get_channel_by_channel_id(channel_id)
    user = get_user_by_token(token)

    # Channel_id does not refer to a valid channel
    if channel is None:
        raise ValueError("Invalid Channel ID")

    # Message is not of appropriate length
    if valid_message(message):
        raise ValueError("Message length too long")

    # User has not joined the channel
    if not channel.is_member(user.u_id):
        raise AccessError("Authorised user is not a member of the channel")

    message_object = global_var.Message(user.u_id, message, channel_id)

    # Append message to channel list
    channel.add_message(message_object)

    return {
        "message_id": message_object.id
    }

@valid_token
def message_remove(token, message_id):
    ''' Given a message ID, the message is removed '''

    channel = get_channel_by_message_id(message_id)
    message = get_message_by_message_id(message_id)
    user = get_user_by_token(token)

    # Message_id does not refer to an existing message
    if not valid_message_id(message_id):
        raise ValueError("Message does not exist")

    # User does not have permission to remove message
    if not message.user_sent_message(user.u_id) and \
        not token_is_admin(token) and \
        not token_is_owner(token) and \
        not channel.is_owner(user.u_id):
        raise AccessError("User does not have permission")

    # Removing message
    channel.remove_message(message_id)

    return {}

@valid_token
def message_edit(token, message_id, message):
    '''
    Given a message, update it's text with new text. If the new message is an
    empty string, the message is deleted.
    '''

    channel = get_channel_by_message_id(message_id)
    message_obj = get_message_by_message_id(message_id)
    user = get_user_by_token(token)

    # message_id does not refer to an existing message
    if not valid_message_id(message_id):
        raise ValueError("Message does not exist")

    # message is not of appropriate length
    if valid_message(message):
        raise ValueError("Message length too long")

    # User does not have permission to edit message
    if not  message_obj.user_sent_message(user.u_id) and \
            not token_is_admin(token) and \
            not token_is_owner(token) and \
            not channel.is_owner(user.u_id):
        raise AccessError("User does not have permission")

    # Edit channel message
    if not message.strip():
        # If empty message, delete
        channel = get_channel_by_message_id(message_id)
        channel.remove_message(message_id)
    else:
        # Otherwise, edit message
        message_obj.edit_message(message)

    return {}

@valid_token
def message_react(token, message_id, react_id):
    '''
    Given a message within a channel the authorised user is part of,
    add a "react" to that particular message
    '''

    channel = get_channel_by_message_id(message_id)
    message_obj = get_message_by_message_id(message_id)
    user = get_user_by_token(token)

    # Message_id does not refer to an existing message
    if not valid_message_id(message_id):
        raise ValueError("Message does not exist")

    # User is not a member of the channel
    if not channel.is_member(user.u_id):
        raise AccessError("Authorised user is not a member of the channel")

    # React_id does not refer to a valid react
    if not valid_react_id(react_id):
        raise ValueError("Invalid React ID")

    # Message already has an react iD
    if message_obj.user_has_reacted(user.u_id, react_id):
        raise ValueError("Message contains an active react")

    # Adding react to message
    message_obj.add_react(user.u_id, react_id)

    return {}

@valid_token
def message_unreact(token, message_id, react_id):
    '''
    Given a message within a channel the authorised user is part of, remove a
    "react" to that particular message
    '''

    channel = get_channel_by_message_id(message_id)
    message_obj = get_message_by_message_id(message_id)
    user = get_user_by_token(token)

    # Message_id does not refer to an existing message
    if not valid_message_id(message_id):
        raise ValueError("Message does not exist")

    # User is not a member of the channel
    if not channel.is_member(user.u_id):
        raise AccessError("Authorised user is not a member of the channel")

    # React_id does not refer to a valid react
    if not valid_react_id(react_id):
        raise ValueError("Invalid React ID")

    # Message already has an react id by the given user
    if not message_obj.user_has_reacted(user.u_id, react_id):
        raise ValueError("Message does not contain an active react")

    # Removing react from message
    message_obj.remove_react(user.u_id, react_id)

    return {}

@valid_token
def message_pin(token, message_id):
    '''
    Given a message within a channel, mark it as "pinned" to be given special
    display treatment by the frontend
    '''

    channel = get_channel_by_message_id(message_id)
    message_obj = get_message_by_message_id(message_id)
    user = get_user_by_token(token)

    # Message_id does not refer to an existing message
    if not valid_message_id(message_id):
        raise ValueError("Message does not exist")

    # Message_id is already pinned
    if message_obj.is_pinned:
        raise ValueError("Message is currently pinned")

    # User is not a member of the channel
    if not channel.is_member(user.u_id):
        raise AccessError("Authorised user is not a member of the channel")

    # User is not an owner of the channel
    if not channel.is_owner(user.u_id) and \
        not token_is_admin(token) and \
        not token_is_owner(token):
        raise ValueError("User is not an admin")

    # Pin message
    message_obj.pin_message()

    return {}

@valid_token
def message_unpin(token, message_id):
    '''
    Given a message within a channel, remove it's mark as unpinned
    '''

    channel = get_channel_by_message_id(message_id)
    message_obj = get_message_by_message_id(message_id)
    user = get_user_by_token(token)

    # Message_id does not refer to an existing message
    if not valid_message_id(message_id):
        raise ValueError("Message does not exist")

    # Message_id is already unpinned
    if not message_obj.is_pinned:
        raise ValueError("Message is currently unpinned")

    # User is not a member of the channel
    if not channel.is_member(user.u_id):
        raise AccessError("Authorised user is not a member of the channel")

    # User is not an owner of the channel
    if not channel.is_owner(user.u_id) and \
        not token_is_admin(token) and \
        not token_is_owner(token):
        raise ValueError("User is not an admin")

    # Unpinning message
    message_obj.unpin_message()

    return {}

def valid_message(message):
    ''' Checks the validity of a message '''
    return len(message) > MAX_MESSAGE_LENGTH


def valid_message_id(message_id):
    ''' Checks the validity of a message id '''
    for channel in global_var.data["channels"]:
        for message in channel.messages:
            if message.id == message_id:
                return True
    return False

def valid_react_id(react_id):
    ''' Checks the validity of a react id '''
    if react_id == LIKE_REACT or react_id == HEART_REACT:
        return True
    return False
