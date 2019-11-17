'''
Channel functions Iteration 2 implementations
Team: You_Things_Can_Choose
'''

import server.global_var as global_var
from server.constants import (LIKE_REACT, LIKE_REACT_INDEX, MAX_CHANNEL_LENGTH,
                              MAX_MESSAGES)
from server.Error import AccessError, ValueError
from server.helpers import (decode_token, get_channel_by_channel_id,
                            get_user_by_token, get_user_by_u_id,
                            token_is_admin, token_is_owner, valid_token)


@valid_token
def channel_invite(token, channel_id, u_id):
    '''
    Invites a user to join a channel
    '''

    channel = get_channel_by_channel_id(channel_id)

    # Channel_id does not refer to a valid channel
    if channel is None:
        raise ValueError("Channel does not exist")

    # Inviting user is not a member of the channel
    if not channel.is_member(decode_token(token)):
        raise AccessError("Authorised user is not a member of the channel")

    # u_id is not a user
    if not get_user_by_u_id(u_id):
        raise ValueError("Invalid User ID")

    # User is added as a member
    channel.add_user(u_id)

    return {}

@valid_token
def channel_details(token, channel_id):
    '''
    Provide basic details about the channel
    '''

    channel = get_channel_by_channel_id(channel_id)

    # channel_id does not refer to a valid channel
    if channel is None:
        raise ValueError("Channel does not exist")

    # user is not a member of the channel
    if not channel.is_member(decode_token(token)):
        raise AccessError("Authorised user is not a member of the channel")

    # Get details regarding the owners and members of the channel
    owners = channel.get_owners_details()
    members = channel.get_members_details()

    # Returns the channel details corresponding to that channel id
    channel_detail = {"name": channel.name, "owner_members": owners, \
        "all_members": members}

    return channel_detail

@valid_token
def channel_messages(token, channel_id, start):
    '''
    Returns up to 50 messages between index "start" and "start + 50".
    Message with 0 index is the most recent message

    end = start + 50

    If function has returned the least recent messages in the channel
    returns -1 in "end" to indicate there are no more msgs to load

    '''

    channel = get_channel_by_channel_id(channel_id)
    u_id = decode_token(token)

    # channel_id does not refer to a valid channel
    if channel is None:
        raise ValueError("Channel does not exist")

    # user is not a member of the channel
    if not channel.is_member(u_id):
        raise AccessError("Authorised user is not a member of the channel")

    # If the start is greater than the number of messages in the channel given
    if start > len(channel.messages):
        raise ValueError("Start index is invalid")

    messages = []

    for i in range(MAX_MESSAGES):
        # End index of -1 to indicate there are no more messages to load
        if start + i >= len(channel.messages):
            return {"messages": messages, "start": start, "end": -1}

        # Gets message object
        message = channel.messages[start + i]

        # Add information regarding if user has reacted to this message
        reacts = message.reacts
        for react in reacts:
            react["is_this_user_reacted"] = \
                message.user_has_reacted(u_id, react['react_id'])

        # Append message dictionary into messages list
        messages.append({
            "message_id": message.id,
            "u_id": message.sender,
            "message": message.message,
            "time_created": message.time_created,
            "reacts": reacts,
            "is_pinned": message.is_pinned,
        })

    # Check which
    if start + MAX_MESSAGES >= len(channel.messages):
        end = -1
    else:
        end = start + MAX_MESSAGES
    return {"messages": messages, "start": start, "end": end}

@valid_token
def channel_leave(token, channel_id):
    '''
    Given a channel ID, the user is removed as a member of the channel
    '''

    channel = get_channel_by_channel_id(channel_id)
    user = get_user_by_token(token)

    # channel_id does not refer to a valid channel
    if channel is None:
        raise ValueError("Channel does not exist")

    # User is removed as a member of the channel
    channel.remove_user(user.u_id)
    channel.remove_owner(user.u_id)

    return {}

@valid_token
def channel_join(token, channel_id):
    '''
    Given a channel_id of a channel that the authorised user can join
    adds them to that channel
    '''

    channel = get_channel_by_channel_id(channel_id)
    user = get_user_by_token(token)

    # channel_id does not refer to a valid channel
    if channel is None:
        raise ValueError("Channel does not exist")

    # User does not have permission to join channel without invite
    if not channel.is_public and \
         not token_is_admin(token) and \
            not token_is_owner(token):
        raise AccessError("Channel is private and user is not admin")

    # User is added to channel
    channel.add_user(user.u_id)

    return {}

@valid_token
def channel_addowner(token, channel_id, u_id):
    '''
    make an user an owner of the channel
    '''

    channel = get_channel_by_channel_id(channel_id)

    # channel_id does not refer to a valid channel
    if channel is None:
        raise ValueError("Channel does not exist")

    # user is already an owner of the channel
    if channel.is_owner(u_id):
        raise ValueError("User is already an owner of the channel")

    # User does not have permission to add owner
    if not channel.is_owner(decode_token(token)) and \
            not token_is_admin(token) and \
            not token_is_owner(token):
        raise AccessError("User is not an owner of the channel or slackrowner")

    # User is added as owner
    channel.add_owner(u_id)

    return {}

@valid_token
def channel_removeowner(token, channel_id, u_id):
    '''
    Remove user with user id u_id an owner of this channel
    '''

    channel = get_channel_by_channel_id(channel_id)

    # channel_id does not refer to a valid channel
    if channel is None:
        raise ValueError("Channel does not exist")

    # user is not an owner of the channel
    if not channel.is_owner(u_id):
        raise ValueError("User id is not an owner of the channel")

    # If the user trying to remove owner does not have permission
    if not channel.is_owner(decode_token(token)) and \
        not token_is_admin(token) and \
        not token_is_owner(token):
        raise AccessError("User is not an owner of the channel or slackrowner")

    channel.remove_owner(u_id)

    return {}

@valid_token
def channels_list(token):
    '''
    Provides a list of all channels and details that the auth user is part of
    '''

    user = get_user_by_token(token)
    channels_user_is_member = []

    # Create a list of channels that the user is apart of
    for channel in global_var.data["channels"]:
        if channel.is_member(user.u_id):
            channels_user_is_member.append({"channel_id": channel.id, \
                                             "name": channel.name})

    return {"channels": channels_user_is_member}

@valid_token
def channels_listall(token):
    '''
    Provides a list of channels and their associated details
    '''

    all_channels = []

    # Creates a list of all channels
    for channel in global_var.data["channels"]:
        all_channels.append({"channel_id": channel.id, \
                                "name": channel.name})

    return {"channels": all_channels}

@valid_token
def channels_create(token, name, is_public):
    '''
    Create a channel with the name that is either public or private
    '''

    # Exception raised
    if len(name) > MAX_CHANNEL_LENGTH:
        raise ValueError("Name is longer than 20 characters")

    user = get_user_by_token(token)

    # A channel object is created
    new_channel = global_var.Channel(name, user.u_id, is_public)

    # channel is added to channels list
    global_var.data["channels"].append(new_channel)

    return {"channel_id": new_channel.id}
