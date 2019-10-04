#Testing for channel_functions
#Created by Ashley Huang
#Created on 2/10/2019

import pytest
from server.channel import channel_functions as func
from server.auth.auth_functions import auth_register
from server.helper.Error import AccessError


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

    assert func.channel_invite(token1, channel_ids, 000) == {}

    #if given an invalid token
    with pytest.raises(ValueError, match = "Invalid token"):
        func.channel_invite("12345", channel_ids, userid2)
    
    #if given an invalid channel_id
    with pytest.raises(ValueError, match = "Invalid channel_id"):
        func.channel_invite(token1, 100, userid2)
    
    #if given an invalid user
    with pytest.raises(ValueError, match = "Invalid user"):
        func.channel_invite(token1, channel_ids, 111111)
    

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
    

    #user 2 create a private channel 
    channel2 = func.channels_create(token2, "TestChannel2", False)
    channel_private = channel2["channel_id"]

    #user 1 joining user2's channel
    assert func.channel_join(token1, channel_ids) == {}


    #if given an invalid channel_id
    with pytest.raises(ValueError, match = "Invalid channel_id"):
        func.channel_join(token1, 100)

    #if channel is private and user is not the admin
    with pytest.raises(AccessError, match = "Channel is private and user is not admin"):
        func.channel_join(token1, channel_private)


def test_channel_addowner():
    

    owner = auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name")
    tokenowner = owner["token"]
    useridowner = owner["u_id"]

    user1 = auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name")
    token1 = user1["token"] 
    userid1 = user1["u_id"]

    user2 = auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name")
    token2 = user2["token"]
    userid2 = user2["u_id"]

    #owner create a channel (123) and is automatically the owner
    channel = func.channels_create(tokenowner, "TestChannel", True)
    channel_ids = channel["channel_id"]

    assert func.channel_addowner("owner", channel_ids, userid1) == {}

    #if given an invalid channel_id
    with pytest.raises(ValueError, match = "Invalid channel_id"):
        func.channel_addowner(token1, 100, useridowner)
    
    #tokenowner made channel, user is already owner of channel
    with pytest.raises(ValueError, match = "User is already an owner of the channel"):
        func.channel_addowner(tokenowner, channel_ids, useridowner)

    #token
    #with pytest.raises(AccessError, match = "Authorised user is not an owner of slackr or an owner of the channel"):
        #func.channel_addowner(token2, channel_ids, userid1)


def test_channel_removeowner():

    user1 = auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name")
    token1 = user1["token"] 
    userid1 = user1["u_id"]

    #user1 create a channel (123) and is automatically the owner
    channel = func.channels_create(user1, "TestChannel", True)
    channel_ids = channel["channel_id"]

    user2 = auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name")
    token2 = user2["token"]
    userid2 = user2["u_id"]

    user3 = auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name")   
    token3 = user3["token"]
    userid3 = user3["u_id"]
    
   

    func.channel_join(token2, channel_ids)
    func.channel_addowner(token1, channel_ids, userid2)

    assert func.channel_removeowner("owner", channel_ids, userid2) == {}

    #if given an invalid channel_id
    with pytest.raises(ValueError, match = "Invalid channel_id"):
        func.channel_removeowner(token1, 100, userid2)

    with pytest.raises(ValueError, match = "User id is not an owner of the channel"):
        func.channel_removeowner(token1, channel_ids, 000)

    with pytest.raises(AccessError, match = "Authorised user is not an owner of slacker, or an owner of the channel"):
        func.channel_removeowner(token3, channel_ids, 100)



def test_channels_list():
    assert func.channels_list(token) == {channels}
    #can use channel join to see if list has changed
    #obtain a valid token, call auth login (returns a valid token)
    #assert this token

#all channels
def test_channels_listall():
    assert func.channels_listall(token) == {channels}


def test_channels_create():
    user1 = auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name")
    token1 = user1["token"] 
    userid1 = user1["u_id"]

    #user1 create a channel (123) and is automatically the owner
    channel = func.channels_create(user1, "TestChannel", True)
    channel_ids = channel["channel_id"]


    assert func.channels_create(token1, "hello world", True) == {"channel_id" : 123}
    assert func.channels_create(token1, "hi world", False) == {"channel_id" : 1}

    with pytest.raises(ValueError, match = "Name is more than 20 characters long"):
        func.channels_create(token1, "asdbcdjsisjd222isjdisjdisjdisjdijsi", True)

    with pytest.raises(ValueError, match = "Name is more than 20 characters long"):
        func.channels_create(token1, "asdbcdjsisjd222isjdisjdisjdisjdijsi", False)

    

   

