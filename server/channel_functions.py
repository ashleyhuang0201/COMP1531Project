'''
Channel functions Iteration 2 implementations
Team: You_Things_Can_Choose
'''
#nothgin
import pytest
import jwt
import server.global_var as global_var
from server.Error import AccessError
import server.helpers as helpers

def channel_invite(token, channel_id, u_id):
    '''
    Invites a user to join a channel
    '''

    channel = helpers.get_channel_by_channel_id(channel_id)

    # Invalid user has accessed function
    if helpers.valid_token(token) == False:
        raise AccessError("Invalid token")

    # Channel_id does not refer to a valid channel
    if channel == None:
        raise ValueError("Channel does not exist")

    # Inviting user is not a member of the channel
    if channel.is_member(helpers.decode_token(token)) == False:
        raise AccessError("Authorised user is not a member of the channel")

    # u_id is not a user
    if helpers.valid_user_id(u_id) == False:
        raise ValueError("User id is not valid")

    # User is added as a member
    channel.add_user(u_id)

    return {}

def channel_details(token, channel_id):
    '''
    Provide basic details about the channel
    '''

    channel = helpers.get_channel_by_channel_id(channel_id)

    # Invalid user has accessed function
    if helpers.valid_token(token) == False:
        raise AccessError("Invalid token")

    # channel_id does not refer to a valid channel
    if channel == None:
        raise ValueError("Channel does not exist")
    
    # user is not a member of the channel
    if channel.is_member(helpers.decode_token(token)) == False:
        raise AccessError("Authorised user is not a member of the channel")

    # Returns the channel details corresponding to that channel id
    channel_details = {"name": channel.name, "owner_members": channel.owners, \
        "all_members": channel.users}

    return channel_details
    

def channel_messages(token, channel_id, start):
    '''
    return up to 50 messages between index "start" and "start + 50".
    Message with 0 index is the most recent message

    end = start + 50

    if function has returned the least recent messages in the channel
    returns -1 in "end" to indicate there are no more msgs to load

    '''

    channel = helpers.get_channel_by_channel_id(channel_id)

    # Invalid user has accessed function
    if helpers.valid_token(token) == False:
        raise AccessError("Invalid token")

    # channel_id does not refer to a valid channel
    if channel == None:
        raise ValueError("Channel does not exist")

    # user is not a member of the channel
    if channel.is_member(helpers.decode_token(token)) == False:
        raise AccessError("Authorised user is not a member of the channel")

    # If the start is greater than the number of messages in the channel given
    if start >= len(channel.messages):
        raise ValueError("Start index is invalid")
    
    messages = []

    for i in range(50):
        if start + i >= len(channel.messages):
            # End index is -1 to indicate there are no more messages to load
            return {"messages": messages, "start": start, "end": -1}
        # Gets message object at index
        message = channel.messages[start + i]
        # Insert additional information regarding reacts
        reacts = message.reacts[0]["is_this_user_reacted"] = \
             message.user_has_reacted(helpers.decode_token(token))

        # Append message dictionary into list
        messages.append({
            "message_id": message.id,
            "u_id": message.sender,
            "message": message.message,
            "time_created": message.time_created,
            "reacts": reacts, 
            "is_pinned": message.is_pinned,
        })

    # End index is the 50th message
    return {"messages": messages, "start": start, "end": start + 49}


def channel_leave(token, channel_id):
    '''
    Given a channel ID, the user is removed as a member of the channel
    '''

    channel = helpers.get_channel_by_channel_id(channel_id)
    user = helpers.get_user_by_token(token)

    # Invalid user has accesed function
    if helpers.valid_token(token) == False:
        raise AccessError("Invalid token")

    # channel_id does not refer to a valid channel
    if channel == None:
        raise ValueError("Channel does not exist")
    
    # User is removed as a member of the channel
    channel.remove_user(user.u_id)
    channel.remove_owner(user.u_id)

    return {}


def channel_join(token, channel_id):
    '''
    Given a channel_id of a channel that the authorised user can join
    adds them to that channel
    '''

    channel = helpers.get_channel_by_channel_id(channel_id)
    user = helpers.get_user_by_token(token)

    # Invalid user has accesed function
    if helpers.valid_token(token) == False:
        raise AccessError("Invalid token")

    # channel_id does not refer to a valid channel
    if channel == None:
        raise ValueError("Channel does not exist")

    # channel is private so invite is required
    if channel.is_public == False and \
            helpers.token_is_admin(token) == False and \
            helpers.token_is_owner(token) == False:
        raise AccessError("Channel is private and user is not admin")

    # User is added to channel
    channel.add_user(user.u_id)

    return {}


def channel_addowner(token, channel_id, u_id):
    '''
    make an user an owner of the channel
    '''

    user = helpers.get_user_by_token(token)
    channel = helpers.get_channel_by_channel_id(channel_id)

    # Invalid user has accesed function
    if helpers.valid_token(token) == False:
        raise AccessError("Invalid token")

    # channel_id does not refer to a valid channel
    if channel == None:
        raise ValueError("Channel does not exist")

    # user is already an owner of the channel
    if channel.is_owner(u_id) == True:
        raise ValueError("User is already an owner of the channel")

    if channel.is_owner(helpers.decode_token(token)) == False and \
            helpers.token_is_admin(token) == False and \
            helpers.token_is_owner(token) == False:
        raise AccessError("User is not an owner of the channel or slackrowner")
    
    # User is added as owner
    channel.add_owner(u_id)

    return {}


def channel_removeowner(token, channel_id, u_id):
    '''
    Remove user with user id u_id an owner of this channel
    '''

    user = helpers.get_user_by_token(token)
    channel = helpers.get_channel_by_channel_id(channel_id)

    # Invalid user has accesed function
    if helpers.valid_token(token) == False:
        raise AccessError("Invalid token")

    # channel_id does not refer to a valid channel
    if channel == None:
        raise ValueError("Channel does not exist")

    # user is not an owner of the channel
    if channel.is_owner(u_id) == False:
        raise ValueError("User id is not an owner of the channel")

    # If the user trying to remove owner does not have permission
    if channel.is_owner(helpers.decode_token(token)) == False and \
            helpers.token_is_admin(token) == False and \
            helpers.token_is_owner(token) == False:
        raise AccessError("User is not an owner of the channel or slackrowner")

    channel.remove_owner(u_id)

    return {}


def channels_list(token):
    '''
    Provides a list of all channels and details that the auth user is part of
    '''    

    # Exception raised
    if helpers.valid_token(token) == False:
        raise AccessError("Invalid token")

    user = helpers.get_user_by_token(token)
    channels_user_is_member = []

    # Create a list of channels that the user is apart of
    for channel in global_var.data["channels"]:
        if channel.is_member(user.u_id):
            channels_user_is_member.append({"channel_id": channel.id, \
                                             "name": channel.name})

    return {"channels": channels_user_is_member}    

def channels_listall(token):
    '''
    Provides a list of channels and their associated details
    '''

    # Exception raised
    if helpers.valid_token(token) == False:
        raise AccessError("Invalid token")

    all_channels = []

    # Creates a list of all channels
    for channel in global_var.data["channels"]:
        all_channels.append({"channel_id": channel.id, \
                                "name": channel.name})

    return {"channels": all_channels}

def channels_create(token, name, is_public):
    '''
    Create a channel with the name that is either public or private
    '''

    # Exception raised
    if len(name) > 20:
        raise ValueError("Name is longer than 20 characters")
    elif helpers.valid_token(token) == False:
        raise AccessError("Invalid token")

    # token is decoded to find user id
    user = helpers.get_user_by_token(token)

    if user == None:
        print("HUH??????")

    # A channel object is created
    new_channel = global_var.Channel(name, user.u_id, is_public)

    # channel is added to channels list
    global_var.data["channels"].append(new_channel)

    return {"channel_id": new_channel.id}



