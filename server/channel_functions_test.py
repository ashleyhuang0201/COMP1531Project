#Testing for channel_functions
#Created by Ashley Huang
#Created on 2/10/2019

import pytest
import channel_functions as func
from auth_functions import auth_register


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
    
'''

def test_channel_details():
    assert func.channel_details(token, channel) == {name, owner_members, all_members}

def test_channel_messages():
    assert func.channel_messages(token, channel, start) == {messages, start, end}

def test_channel_leave():
    assert func.channel_leave(token, channel) == {}
    #call channel_list(token) 
    #use assert to check whether the user is removed

def test_channel_join():
    assert func.channel_join(token, channel) == {}

def test_channel_addowner():
    assert func.channel_addowner(token, channel, id) == {}

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