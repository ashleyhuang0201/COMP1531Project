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

'''
Provide basic details about the channel

ValueError:
- channel_id does not exist

AccessError:
- authorised user is not a member of channel (channel_id)
'''

def channel_details(token, channel_id):
    pass

def channel_messages(token, channel_id, start):
    pass

def channel_leave(token, channel_id):
    pass

def channel_join(token, channel_id):
    pass


def channel_addowner(token, channel_id, u_id):
    pass

def channel_removeowner(token, channel_id, u_id):
    pass

def channels_list(token):
    pass

def channels_listall(token):
    pass

def channels_create(token, name, is_public):
    pass

#Checks if the channel is a valid channel
def valid_channel(channel_id):
    pass




