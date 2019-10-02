# Dummy implementations of channel_functions
# Implemented by: Ashley Huang
# Created on: 1/10/2019

import pytest

'''
Invites a user with user id u_id to join a channel (channel_id_)

ValueError: 
-when channel_id does not refer to a valid channel that the user is part of
-u_id does not refer to a valid user

'''
def channel_invite(token, channel_id, u_id):
    if valid_channel(channel_id) == False:
        raise ValueError("Channel is not valid")
    if valid_user(u_id) == False:
        raise ValueError("User id is not valid")

    return {}
'''
Provide basic details about the channel

ValueError:
- channel_id does not exist

AccessError:
- authorised user is not a member of channel (channel_id)
'''

def channel_details(token, channel_id):
    if valid_channel(channel_id) == False:
        raise ValueError("Channel does not exist")
    
    if valid_member(token, channel_id) == False:
        raise AccessError("Authorised user is not a member of the channel")

    #returned details 
    channel_details = {"name" : "Channel name", "owner_members": "Ethan Jack", "all_members": "Ethan Jack, Jack Smith"}

    return channel_details
    
'''
return up to 50 messages between index "start" and "start + 50".
Message with 0 index is the most recent message

end = start + 50

if function has returned the least recent messages in the channel
returns -1 in "end" to indicate there are no more msgs to load

ValueError:
- channel_id does not exist
- start is greater than the total number of msgs in the channel

AccessError:
if user is not a member of the channel of channel_id
'''
def channel_messages(token, channel_id, start):
    if valid_member(token, channel_id) == False:
        raise AccessError("Authorised user is not a member of the channel")
    if valid_channel(channel_id) == False:
        raise ValueError("Channel does not exist")
    if start > length(messages)
        raise ValueError("Message does not exist")

    return messages, start, end
    
'''
Given a channel ID, the user is removed as a member of the channel
ValueError:
- if channel_id does not exist
'''
def channel_leave(token, channel_id):
    if valid_channel(channel_id) == False:
        raise ValueError("Channel does not exist")
    
    return {}
    
'''
Given a channel_id of a channel that the authorised user can join
adds them to that channel
ValueError:
- if channel_id does not exist
AccessError:
- if channel_id refers to a channel that is private (when the authorised user is not an admin)
'''
def channel_join(token, channel_id):
    if valid_channel(channel_id) == False:
        raise ValueError("Channel does not exist")
    if private_channel(channel_id) == True:
        raise AccessError("Channel is private")

    return {}
'''
make user an owner of the channel

ValueError:
- if channel does not exist
- when user is already the owner of the channel

AccessError:
- when the authorised user is not an owner of the slackr, or an owner of the channel
'''
def channel_addowner(token, channel_id, u_id):
    if valid_channel(channel_id) == False:
        raise ValueError("Channel does not exist")
    if user_is_owner(channel_id, u_id) == True:
        raise ValueError("User is already the owner of the channel")
    if user_is_owner(channel_id, token) == False or user_is_slackrowner(token) == False:
        raise AccessError("User is not an owner of slackr or an owner of the channel")
    
    return {}

'''
Remove user with user id u_id an owner of this channel
ValueError:
- if channel_id does not exist
- when user with u_id is not an owner of the channel

AccessError:
- when authorised user is not an owner of slackr, or an owner of the channel

'''
def channel_removeowner(token, channel_id, u_id):
    if valid_channel(channel_id) == False:
        raise ValueError("Channel does not exist")
    if user_is_owner(channel_id, u_id) == False:
        raise ValueError("User is not an owner of the channel")
    if user_is_owner(channel_id, token) == False or user_is_slackrowner(token) == False:
        raise AccessError("User is not an owner of slackr or an owner of the channel")

    return {}

'''
Provides a list of all channels and details that the authorised user is part of
'''
def channels_list(token):
    #if user token is part of channels 
    #return channels
    return channels
'''
Provides a list of channels and their associated details
'''
def channels_listall(token):
    return channels

'''
Create a channel with the name that is either public or private
ValueError:
- name is more than 20 characters long

'''
def channels_create(token, name, is_public):
    if len(name) > 20
        ValueError("Name is longer than 20 characters")
    return channel_id
    

#Checks if the channel is a valid channel
def valid_channel(channel_id):
    if channel_id == "id":
        return True
    else:
        return False


#Checks if the user is a member of the channel
def valid_member(token, channel_id):
    #if user is a member of the channel
    if token == "all_members" :
        return True
    else:
        return False



#Returns true if it is a private channel, returns false if not private
def private_channel(channel_id):
    if channel_id == "private_channel":
        return True
    else:
        return False
    
def user_is_owner(channel_id, token):
    pass
    
def user_is_slackrowner(token):
    pass

