#Testing for channel_functions
#Created by Ashley Huang
#Created on 2/10/2019

import pytest
from server.channel import channel_functions as func
from server.auth.auth_functions import auth_register
from server.helper.Error import AccessError
from server.message.message_functions import message_send
from server.search.search_function import search


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
        func.channel_invite(token1, channel_ids, 111111)
    

def test_channel_details():
    
    user1 = auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name")
    token1 = user1["token"]
    userid1 = user1["u_id"]

    #if user is not a member of the channel, has not joined yet
    with pytest.raises(AccessError, match = "Authorised user is not a member of the channel"):
        func.channel_details("12345", channel_ids)

    #token1 creates a channel and is automatically part of it as the owner
    channel = func.channels_create(token1, "TestChannel", True)
    channel_ids = channel["channel_id"]

    assert func.channel_details(token1, channel_ids) == {"name" : "ChannelName", "owner_members": {"u_id": userid1, "name_first": "valid_correct_first_name" , "name_last": "valid_correct_last_name"}, "all_members": {"u_id": userid1 , "name_first": "valid_correct_first_name" , "name_last": "valid_correct_last_name"}}
    
    #if given an invalid channel_id
    with pytest.raises(ValueError, match = "Invalid channel_id"):
        func.channel_details(token1, 100)

    
def test_channel_messages():
    user1 = auth_register("channel_messages@test.com", "password", "channel_messages", "test")
    token1 = user1["token"]

    user2 = auth_register("channel_messages@test2.com", "password", "channel_messages2", "test2")
    token2 = user1["token"]

    #create a channel 
    channel = func.channels_create(token1, "TestChannel", True)
    channel_id = channel["channel_id"]

    # test correct response when no messages in channel
    assert func.channel_messages(token1, channel_id, 0) == {"messages": [], "start": 0, "end": -1}

    # send a message to the channel and check that return is correct
    message_send(token1, channel_id, 'Channel_messages_test_message_192746583745928792374')
    search_result = search(token1, 'Channel_messages_test_message_192746583745928792374')
    sent_message = search_result['messages']
    assert func.channel_messages(token1, channel_id, 0) == {"messages": {sent_message[0]}, "start": 0, "end": -1}

    # test exceptions
    with pytest.raises(ValueError, match = "Channel does not exist"):
        func.channel_messages(token1, -1, 0)
    
    with pytest.raises(ValueError, match = "Start index is invalid"):
        func.channel_message(token1, channel_id, 100)

    with pytest.raises(AccessError, match = "User is not a member of the channel"):
        func.channel_message(token2, channel_id, 0)

    

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

    #token1 joins channel that owner created
    func.channel_join(token1, channel_ids)

    assert func.channel_addowner("owner", channel_ids, userid1) == {}
    
    #if given an invalid channel_id
    with pytest.raises(ValueError, match = "Invalid channel_id"):
        func.channel_addowner(tokenowner, 100, userid1)

    #token is not an owner of the channel
    with pytest.raises(AccessError, match = "Authorised user is not an owner of the channel"):
        func.channel_addowner(token1, channel_ids, userid2)

    #add token1 as an owner
    func.channel_addowner(tokenowner, channel_ids, userid1)

    #token1/userid1 is already an owner of the channel
    with pytest.raises(ValueError, match = "User is already an owner of the channel"):
        func.channel_addowner(tokenowner, channel_ids, userid1)

    



def test_channel_removeowner():

    user1 = auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name")
    token1 = user1["token"] 
    userid1 = user1["u_id"]

    #token1 create a channel (123) 
    channel = func.channels_create(token1, "TestChannel", True)
    channel_ids = channel["channel_id"]

    user2 = auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name")
    token2 = user2["token"]
    userid2 = user2["u_id"]

    #token2 joins the channel token1 made
    func.channel_join(token2, channel_ids)
    
    #user2 is not the owner, thus trying to removeowner raises an error
    with pytest.raises(ValueError, match = "User id is not an owner of the channel"):
        func.channel_removeowner(token1, channel_ids, 000)
    
    #token1 makes token2 the owner
    func.channel_addowner(token1, channel_ids, userid2)
    
    assert func.channel_removeowner(token1, channel_ids, userid2) == {}

    #if given an invalid channel_id
    with pytest.raises(ValueError, match = "Invalid channel_id"):
        func.channel_removeowner(token1, 100, userid2)

  


def test_channels_list():

    user1 = auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name")
    token1 = user1["token"] 
    userid1 = user1["u_id"]

    user2 = auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name")
    token1 = user2["token"] 
    userid2 = user2["u_id"]

    #user1 create a channel (123)
    channel = func.channels_create(token1, "TestChannel", True)
    channel_ids = channel["channel_id"]

    #user2 create a channel (123)
    channel2 = func.channels_create(token2, "TestChannel2", True)
    channel_ids2 = channel2["channel_id"]
   
    assert func.channels_list(token1) == {"id" : 123, "name" : "TestChannel"}

    assert func.channels_list(token2) == {"id" : 123, "name" : "TestChannel2"}

    #user2 creates another channel
    channel3 = func.channels_create(token2, "TestChannel3", True)
    channel_ids3 = channel3["channel_id"]
    
    #assert token2 is in two channels
    assert func.channels_list(token2) == {"id" : 123, "name" : "TestChannel2"}, {"id" : 123, "name" : "TestChannel3"}

def test_channels_listall():

    user1 = auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name")
    token1 = user1["token"] 
    userid1 = user1["u_id"]

    channel = func.channels_create(token1, "TestChannel1", True)
    channel_ids = channel["channel_id"]

    assert func.channels_list(token1) == {"id" : 123, "name" : "TestChannel1"}
    
    #creating another channel
    channel2 = func.channels_create(token1, "TestChannel2", False)
    channel_ids = channel2["channel_id"]
    
    assert func.channels_list(token1) == {"id": 123, "name" : "TestChannel1"}, {"id": 1, "name": "TestChannel2"}
    
    #if given invalid token 
    with pytest.raises(ValueError, match = "Invalid token"):
        func.channels_listall("12345")

def test_channels_create():
    user1 = auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name")
    token1 = user1["token"] 
    userid1 = user1["u_id"]

    #user1 create a channel  
    channel = func.channels_create(user1, "TestChannel", True)
    channel_ids = channel["channel_id"]

    assert func.channels_create(token1, "Channel1", True) == {"channel_id" : 123}
    assert func.channels_create(token1, "Channel2", False) == {"channel_id" : 1}

    #public channel, name longer than 20 characters
    with pytest.raises(ValueError, match = "Name is more than 20 characters long"):
        func.channels_create(token1, "asdbcdjsisjd222isjdisjdisjdisjdijsi", True)

    #private channel, name longer than 20 characters
    with pytest.raises(ValueError, match = "Name is more than 20 characters long"):
        func.channels_create(token1, "asdbcdjsisjd222isjdisjdisjdisjdijsi", False)

    

