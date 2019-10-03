#Testing for channel_functions
#Created by Ashley Huang
#Created on 2/10/2019

import pytest
import channel_functions as func
from auth_functions import auth_register
from Error import AccessError


def test_channel_invite():
    #the authorised user
    user1 = auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name")
    token1 = user1["token"]

    #the one being invited
    user2 = auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name")
    userid2 = user2["u_id"]

    #create a channel 
    channel = func.channels_create(token1, "TestChannel", True)
    channel_ids = channel["channel_id"]

    assert func.channel_invite(token1, channel_ids, userid2) == {}

    #if given an invalid token
    with pytest.raises(ValueError, match = "Invalid token"):
        func.channel_invite("12345", channel_ids, userid2)
    
    #if given an invalid channel_id
    with pytest.raises(ValueError, match = "Invalid channel_id"):
        func.channel_invite(token1, 100, userid2)
    
    #if given an invalid user
    with pytest.raises(ValueError, match = "Invalid user"):
        func.channel_invite(token1, channel_ids, "invalid_id")
    

def test_channel_details():
    
    user1 = auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name")
    token1 = user1["token"]

    #create a channel 
    channel = func.channels_create(token1, "TestChannel", True)
    channel_ids = channel["channel_id"]

    assert func.channel_details(token1, channel_ids) == {"name" : "ChannelName", "owner_members": "Ethan Jack", "all_members": "Ethan Jack, Jack Smith"}
    
    #if user is not a member of the channel
    with pytest.raises(AccessError, match = "Authorised user is not a member of the channel"):
        func.channel_details("12345", channel_ids)
   
    #if given an invalid channel_id
    with pytest.raises(ValueError, match = "Invalid channel_id"):
        func.channel_details(token1, 100)

    
    
'''
def test_channel_messages():

    user1 = auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name")
    token1 = user1["token"]

    #create a channel 
    channel = func.channels_create(token1, "TestChannel", True)
    channel_ids = channel["channel_id"]
    FIX DIS REEEEE
    assert func.channel_messages(token, channel, start) == {messages, start, end}

    with pytest.raises(ValueError, match = "Invalid channel_id"):
        func.channel_messages(token1, 100, start)

    
'''
def test_channel_leave():
    #can an owner leave channel
    user1 = auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name")
    token1 = user1["token"]

    #create a channel 
    channel = func.channels_create(token1, "TestChannel", True)
    channel_ids = channel["channel_id"]

    assert func.channel_leave(token1, channel_ids) == {}

    #if given an invalid channel_id
    with pytest.raises(ValueError, match = "Invalid channel_id"):
        func.channel_leave(token1, 100)


    #call channel_list(token) ?? from piazza
    #use assert to check whether the user is removed???

def test_channel_join():

    user1 = auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name")
    token1 = user1["token"]

    user2 = auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name")
    token2 = user2["token"]
    userid2 = user2["u_id"]

    #user 2 create a channel 
    channel = func.channels_create(token2, "TestChannel", True)
    channel_ids = channel["channel_id"]

    #user 2 create a channel 
    channel2 = func.channels_create(token2, "TestChannel2", False)
    channel_private = channel2["channel_id"]

    #user 1 joining user2's channel
    assert func.channel_join(token1, channel_ids) == {}


    #if given an invalid channel_id
    with pytest.raises(ValueError, match = "Invalid channel_id"):
        func.channel_join(token1, 100)

    #if channel is private and user is not the admin
    #with pytest.raises(AccessError, match = "Channel is private and user is not admin"):
        #func.channel_join(token1, channel_private)
    # WHY DOESNT DIS WORK YIKES


def test_channel_addowner():
    user1 = auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name")
    token1 = user1["token"]
    userid1 = user1["u_id"]

    user2 = auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name")
    token2 = user2["token"]
    userid2 = user2["u_id"]

    #user 1 create a channel (123)
    channel = func.channels_create(token1, "TestChannel", True)
    channel_ids = channel["channel_id"]

    #assert func.channel_addowner(token1, channel_ids, userid2) == {}

'''
def test_channel_removeowner():
    assert func.channel_removeowner(token, channel, id) == {}

#authorised user is part of
def test_channels_list():
    assert func.channels_list(token) == {channels}
    #can use channel join to see if list has changed
    #obtain a valid token, call auth login (returns a valid token)
    #assert this token

#all channels
def test_channels_listall():
    assert func.channels_listall(token) == {channels}

def test_channels_create():
    assert func.channels_create(token, name, is_public) == {channel}
'''