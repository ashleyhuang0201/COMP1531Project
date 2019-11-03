'''
Message functions Iteration 2 implementations
Team: You_Things_Can_Choose
'''
import datetime
from threading import Timer

import server.global_var as global_var
from server.Error import AccessError
import server.helpers as helpers


def message_sendlater(token, channel_id, message, time_sent):
    '''
    Sends a message from authorised_user to the channel specified by
    channel_id automatically at a specified time in the future
    '''

    channel = helpers.get_channel_by_channel_id(channel_id)
    user = helpers.get_user_by_token(token)

    # Invalid user has accessed function
    if not helpers.valid_token(token):
        raise AccessError("Invalid token")

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
    Timer(time_diff, message_send, args=[token, channel_id, message_object]).start()

    return {
        "message_id": message_object.id
    }

def message_send(token, channel_id, message):
    '''
    Send a message from authorised_user to the channel specified by channel_id
    '''

    channel = helpers.get_channel_by_channel_id(channel_id)
    user = helpers.get_user_by_token(token)

    # Invalid user has accessed function
    if not helpers.valid_token(token):
        raise AccessError("Invalid token")

    # Channel_id does not refer to a valid channel
    if channel is None:
        print(f"tried to send to {channel_id}")
        raise ValueError("Invalid Channel ID")

    # Message is not of appropriate length
    if valid_message(message):
        raise ValueError("Message length too long")

    # User has not joined the channel
    if not channel.is_member(user.u_id):
        raise AccessError("Authorised user is not a member of the channel")

    # If passing a string then create a new message object otherwise use the
    # message object given
    if type(message) == str:
        # Create new message object
        message_object = global_var.Message(user.u_id, message, channel_id)
    else:
        message_object = message

    # Append message to channel list
    channel.add_message(message_object)

    return {
        "message_id": message_object.id
    }

def message_remove(token, message_id):
    '''
    Given a message ID, the message is removed
    '''

    channel = helpers.get_channel_by_message_id(message_id)
    message = helpers.get_message_by_message_id(message_id)
    user = helpers.get_user_by_token(token)

    # Invalid user has accessed function
    if not helpers.valid_token(token):
        raise AccessError("Invalid token")

    # Message_id does not refer to an existing message
    if not valid_message_id(message_id):
        raise ValueError("Message does not exist")

    # User does not have permission to remove message
    if not message.user_sent_message(user.u_id) and \
        not helpers.token_is_admin(token) and \
        not helpers.token_is_owner(token) and \
        not channel.is_owner(user.u_id):
        raise AccessError("User does not have permission")

    # Removing message
    channel.remove_message(message_id)

    return {}

def message_edit(token, message_id, message):
    '''
    Given a message, update it's text with new text
    '''

    channel = helpers.get_channel_by_message_id(message_id)
    message_obj = helpers.get_message_by_message_id(message_id)
    user = helpers.get_user_by_token(token)

    # Invalid user has accessed function
    if not helpers.valid_token(token):
        raise AccessError("Invalid token")

    # message_id does not refer to an existing message
    if not valid_message_id(message_id):
        raise ValueError("Message does not exist")

    # message is not of appropriate length
    if valid_message(message):
        raise ValueError("Message length too long")

    # User does not have permission to edit message
    if not  message_obj.user_sent_message(user.u_id) and \
            not helpers.token_is_admin(token) and \
            not helpers.token_is_owner(token) and \
            not channel.is_owner(user.u_id):
        raise AccessError("User does not have permission")

    # Edit channel message
    message_obj.edit_message(message)

    return {}

def message_react(token, message_id, react_id):
    '''
    Given a message within a channel the authorised user is part of, add a "react"
    to that particular message
    '''

    channel = helpers.get_channel_by_message_id(message_id)
    message_obj = helpers.get_message_by_message_id(message_id)
    user = helpers.get_user_by_token(token)

    # Invalid user has accessed function
    if not helpers.valid_token(token):
        raise AccessError("Invalid token")

    # Message_id does not refer to an existing message
    if not valid_message_id(message_id):
        raise ValueError("Message does not exist")

    # React_id does not refer to a valid react
    if not valid_react_id(react_id):
        raise ValueError("Invalid React ID")

    # Message already has an react iD
    if message_obj.user_has_reacted(user.u_id):
        raise ValueError("Message contains an active react")

    # User is not a member of the channel
    if not channel.is_member(user.u_id):
        raise AccessError("Authorised user is not a member of the channel")

    # Adding react to message
    message_obj.add_react(user.u_id)

    return {}

def message_unreact(token, message_id, react_id):
    '''
    Given a message within a channel the authorised user is part of, remove a
    "react" to that particular message
    '''

    channel = helpers.get_channel_by_message_id(message_id)
    message_obj = helpers.get_message_by_message_id(message_id)
    user = helpers.get_user_by_token(token)

    # Invalid user has accessed function
    if not helpers.valid_token(token):
        raise AccessError("Invalid token")

    # Message_id does not refer to an existing message
    if not valid_message_id(message_id):
        raise ValueError("Message does not exist")

    # React_id does not refer to a valid react
    if not valid_react_id(react_id):
        raise ValueError("Invalid React ID")

    # Message already has an react iD
    if not message_obj.user_has_reacted(user.u_id):
        raise ValueError("Message does not contain an active react")

    # User is not a member of the channel
    if not channel.is_member(user.u_id):
        raise AccessError("Authorised user is not a member of the channel")

    # Removing react from message
    message_obj.remove_react(user.u_id)

    return {}

def message_pin(token, message_id):
    '''
    Given a message within a channel, mark it as "pinned" to be given special
    display treatment by the frontend
    '''

    channel = helpers.get_channel_by_message_id(message_id)
    message_obj = helpers.get_message_by_message_id(message_id)
    user = helpers.get_user_by_token(token)

    # Invalid user has accessed function
    if not helpers.valid_token(token):
        raise AccessError("Invalid token")

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
        not helpers.token_is_admin(token) and \
        not helpers.token_is_owner(token):
        raise ValueError("User is not an admin")

    # Pin message
    message_obj.pin_message()

    return {}

def message_unpin(token, message_id):
    '''
    Given a message within a channel, remove it's mark as unpinned
    '''

    channel = helpers.get_channel_by_message_id(message_id)
    message_obj = helpers.get_message_by_message_id(message_id)
    user = helpers.get_user_by_token(token)

    # Invalid user has accessed function
    if not helpers.valid_token(token):
        raise AccessError("Invalid token")

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
        not helpers.token_is_admin(token) and \
        not helpers.token_is_owner(token):
        raise ValueError("User is not an admin")

    # Unpinning message
    message_obj.unpin_message()

    return {}

def valid_message(message):
    '''
    Checks the validity of a message
    '''
    return len(message) > 1000


def valid_message_id(message_id):
    '''
    Checks the validity of a message id
    '''
    for channel in global_var.data["channels"]:
        for message in channel.messages:
            if message.id == message_id:
                return True
    return False

def valid_react_id(react_id):
    '''
    Checks the validity of a react id
    '''
    if react_id == 1:
        return True
    return False
