# Dummy implementations of channel_functions
# Implemented by: Ashley Huang
# Created on: 1/10/2019

import pytest
from server.helper.Error import AccessError

#Invites a user with user id u_id to join a channel (channel_id)

def channel_invite(token, channel_id, u_id):
    if valid_channel(channel_id) == False:
        raise ValueError("Channel is not valid")
    if valid_member(token, channel_id) == False:
        raise ValueError("User is not part of the channel")
    if valid_user(u_id) == False:
        raise ValueError("User id is not valid")

    return {}

#Provide basic details about the channel

def channel_details(token, channel_id):
    if valid_channel(channel_id) == False:
        raise ValueError("Channel does not exist")
    
    if valid_member(token, channel_id) == False:
        raise AccessError("Authorised user is not a member of the channel")

    #returned details 
    channel_details = {"name" : "ChannelName", "owner_members":\
     {"u_id": "userID", "name_first": "valid_correct_first_name" , \
     "name_last": "valid_correct_last_name"}, "all_members": {"u_id": "UserID" \
     , "name_first": "valid_correct_first_name" , "name_last": \
     "valid_correct_last_name"}}

    return channel_details
    
'''
return up to 50 messages between index "start" and "start + 50".
Message with 0 index is the most recent message

end = start + 50

if function has returned the least recent messages in the channel
returns -1 in "end" to indicate there are no more msgs to load

'''
def channel_messages(token, channel_id, start):
    messages = []

    if valid_channel(channel_id) == False:
        raise ValueError("Channel does not exist")
    if start > len(messages):
        raise ValueError("Start index is invalid")
    if valid_member(token, channel_id) == False:
        raise AccessError("User is not a member of the channel")
    
    output = {"messages" : messages, "start": 0,"end" : 50}

    return output

#Given a channel ID, the user is removed as a member of the channel
def channel_leave(token, channel_id):
    if valid_channel(channel_id) == False:
        raise ValueError("Channel does not exist")
    
    return {}

#Given a channel_id of a channel that the authorised user can join
#adds them to that channel
def channel_join(token, channel_id):
    if valid_channel(channel_id) == False:
        raise ValueError("Channel does not exist")
    if private_channel(channel_id) == True:
        raise AccessError("Channel is private")

    return {}

#make user an owner of the channel
def channel_addowner(token, channel_id, u_id):
    if valid_channel(channel_id) == False:
        raise ValueError("Channel does not exist")
    if user_is_owner(channel_id, u_id) == True:
        raise ValueError("User is already the owner of the channel")
    if token_is_slackrowner(token) == False and \
    token_is_owner(channel_id, token) == False:
        raise AccessError("User is not an owner of the channel or slackrowner")
    
    return {}


#Remove user with user id u_id an owner of this channel
def channel_removeowner(token, channel_id, u_id):
    if valid_channel(channel_id) == False:
        raise ValueError("Channel does not exist")
    if user_is_owner(channel_id, u_id) == False:
        raise ValueError("User is not an owner of the channel")
    if token_is_owner(channel_id, token) == False and \
    token_is_slackrowner(token) == False:
        raise AccessError("User is not an owner of the channel or slackrowner")
    return {}

#Provides a list of all channels and details that the auth user is part of
def channels_list(token):
    #if token is part of channels 
    
    channels = {"id" : 123, "name" : "TestChannel"}
    return channels

#Provides a list of channels and their associated details
def channels_listall(token):
    channels = {"id" : 123, "name" : "TestChannel"}

    return channels

#Create a channel with the name that is either public or private
def channels_create(token, name, is_public):
    if len(name) > 20:
        raise ValueError("Name is longer than 20 characters")
    elif is_public == True:
        return {"channel_id": 123}
    else:
        #if private
        return {"channel_id" : 1}

#Checks if the channel is a valid channel
def valid_channel(channel_id):
    if channel_id == 123 or channel_id == 1:
        return True
    else:
        return False

#Checks if the user is a member of the channel
def valid_member(token, channel_id):
    if token == "valid_token" or token == "valid_u_id" or \
    token == "slackrowner" or token == "owner" and \
    (channel_id == 123 or channel_id == 1) :
        return True
    else:
        return False

#Returns true if it is a private channel, returns false if not private
def private_channel(channel_id):
    if channel_id == 1:
        return True
    else:
        return False
    
#if user with u_id is an owner of channel, return true
def user_is_owner(channel_id, u_id):
    if u_id == 100 and channel_id == 123:
        return True
    else:
        return False
    
#if authorised user is slackr owner, return true, else return false
def token_is_slackrowner(token):
    if token == "slackrowner":
        return True
    else:
        return False

#if authorised user is the owner of a channel, return true
def token_is_owner(channel_id, token):
    if token == "owner" and (channel_id == 123 or channel_id == 1):
        return True
    else:
        return False

def valid_user(u_id):
    if u_id == 000 or u_id == 100 or u_id == "valid_u_id":
        return True
    else:
        return False
