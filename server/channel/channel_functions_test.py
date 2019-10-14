'''
Testing for channel_functions
Created by Ashley Huang
Created on 2/10/2019
'''

import pytest
from server.channel import channel_functions as func
from server.auth.auth_functions import auth_register
from server.helper.Error import AccessError
from server.message.message_functions import message_send
from server.search.search_function import search

def test_channel_invite():
    '''
    Function tests for channel_invite
    '''
    #Initialisation
    user1 = auth_register("valid_correct_email@test.com", \
    "valid_correct_password", "valid_correct_first_name", \
    "valid_correct_last_name")
    token1 = user1["token"]

    #the one being invited
    user2 = auth_register("valid_correct_email@test2.com", \
    "valid_correct_password", "valid_correct_first_name",\
     "valid_correct_last_name")
    userid2 = user2["u_id"]

    #create a channel
    channel = func.channels_create(token1, "TestChannel", True)
    channel_ids = channel["channel_id"]

    assert func.channel_invite(token1, channel_ids, userid2) == {}

    #if given an invalid token
    with pytest.raises(ValueError, match="Invalid token"):
        func.channel_invite("12345", channel_ids, userid2)

    #if given an invalid channel_id
    with pytest.raises(ValueError, match="Invalid channel_id"):
        func.channel_invite(token1, 100, userid2)

    #if given an invalid user
    with pytest.raises(ValueError, match="Invalid user"):
        func.channel_invite(token1, channel_ids, 111111)

def test_channel_details():
    '''
    Function tests for channel_details
    '''
    #initialisation
    user1 = auth_register("valid_correct_email@test.com", \
    "valid_correct_password", "valid_correct_first_name", \
    "valid_correct_last_name")
    token1 = user1["token"]
    userid1 = user1["u_id"]

    #token1 creates a channel and is automatically part of it as the owner
    channel = func.channels_create(token1, "TestChannel", True)
    channel_ids = channel["channel_id"]

    #if user is not a member of the channel, has not joined yet
    with pytest.raises(AccessError, match=\
    "User is not a member of the channel"):
        func.channel_details("12345", channel_ids)

    assert func.channel_details(token1, channel_ids) == \
    {"name" : "ChannelName", "owner_members": {"u_id": userid1, \
    "name_first": "valid_correct_first_name", "name_last": \
    "valid_correct_last_name"}, "all_members": {"u_id": userid1, \
    "name_first": "valid_correct_first_name", "name_last": \
    "valid_correct_last_name"}}

    #if given an invalid channel_id
    with pytest.raises(ValueError, match="Invalid channel_id"):
        func.channel_details(token1, 100)

def test_channel_messages():
    '''
    Function tests for channel_messages
    '''
    #initialisation
    user1 = auth_register("channel_messages@test.com", "password", \
    "channel_messages", "test")
    token1 = user1["token"]

    user2 = auth_register("channel_messages@test2.com", "password", \
    "channel_messages2", "test2")
    token2 = user2["token"]

    #create a channel
    channel = func.channels_create(token1, "TestChannel", True)
    channel_id = channel["channel_id"]

    # test correct response when no messages in channel
    assert func.channel_messages(token1, channel_id, 0) == \
    {"messages": [], "start": 0, "end": -1}

    # send a message to the channel and check that return is correct
    message_send(token1, channel_id, \
    'Channel_messages_test_message_192746583745928792374')

    search_result = search(token1, \
    'Channel_messages_test_message_192746583745928792374')

    sent_message = search_result['messages']

    assert func.channel_messages(token1, channel_id, 0) == \
    {"messages": {sent_message[0]}, "start": 0, "end": -1}

    # test exceptions
    with pytest.raises(ValueError, match="Channel does not exist"):
        func.channel_messages(token1, -1, 0)

    with pytest.raises(ValueError, match="Start index is invalid"):
        func.channel_messages(token1, channel_id, 100)

    with pytest.raises(AccessError, match=\
    "User is not a member of the channel"):
        func.channel_messages(token2, channel_id, 0)

def test_channel_leave():
    '''
    Function tests for channel_leave
    '''
    #initialisation
    user1 = auth_register("valid_correct_email@test.com", \
    "valid_correct_password", "valid_correct_first_name", \
    "valid_correct_last_name")
    token1 = user1["token"]

    #create a channel
    channel = func.channels_create(token1, "TestChannel", True)
    channel_ids = channel["channel_id"]

    assert func.channel_leave(token1, channel_ids) == {}

    #if given an invalid channel_id
    with pytest.raises(ValueError, match="Invalid channel_id"):
        func.channel_leave(token1, 100)

def test_channel_join():
    '''
    Function tests for channel_join
    '''
    #initialisation
    user1 = auth_register("valid_correct_email@test.com", \
    "valid_correct_password", "valid_correct_first_name",\
     "valid_correct_last_name")
    token1 = user1["token"]

    user2 = auth_register("valid_correct_email@test2.com", \
    "valid_correct_password", "valid_correct_first_name", \
    "valid_correct_last_name")
    token2 = user2["token"]

    #user 2 create a channel
    channel = func.channels_create(token2, "TestChannel", True)
    channel_ids = channel["channel_id"]

    #user 2 create a private channel
    channel2 = func.channels_create(token2, "TestChannel2", False)
    channel_private = channel2["channel_id"]


    assert func.channel_join(token1, channel_ids) == {}

    #if given an invalid channel_id
    with pytest.raises(ValueError, match="Invalid channel_id"):
        func.channel_join(token1, 100)

    #if channel is private and user is not the admin
    with pytest.raises(AccessError, match=\
    "Channel is private and user is not admin"):
        func.channel_join(token1, channel_private)

def test_channel_addowner():
    '''
    Function tests for channel_addowner
    '''

    owner = auth_register("valid_correct_email@test.com", \
    "valid_correct_password", "valid_correct_first_name", \
    "valid_correct_last_name")
    tokenowner = owner["token"]

    user1 = auth_register("valid_correct_email@test1.com", \
    "valid_correct_password", "valid_correct_first_name",\
     "valid_correct_last_name")
    token1 = user1["token"]
    userid1 = user1["u_id"]

    user2 = auth_register("valid_correct_email@test2.com",\
     "valid_correct_password", "valid_correct_first_name", \
     "valid_correct_last_name")
    userid2 = user2["u_id"]

    #owner creates a channel and is automatically the owner
    channel = func.channels_create(tokenowner, "TestChannel", True)
    channel_ids = channel["channel_id"]

    #token1 joins channel that owner created
    func.channel_join(token1, channel_ids)

    assert func.channel_addowner("owner", channel_ids, userid1) == {}

    #if given an invalid channel_id
    with pytest.raises(ValueError, match="Invalid channel_id"):
        func.channel_addowner(tokenowner, 100, userid1)

    #token is not an owner of the channel
    with pytest.raises(AccessError, match=\
    "User is not an owner of the channel"):
        func.channel_addowner(token1, channel_ids, userid2)

    #add token1 as an owner
    func.channel_addowner(tokenowner, channel_ids, userid1)

    #token1/userid1 is already an owner of the channel
    with pytest.raises(ValueError, match=\
    "User is already an owner of the channel"):
        func.channel_addowner(tokenowner, channel_ids, userid1)

def test_channel_removeowner():
    '''
    Function tests for channel_removeowner
    '''

    user1 = auth_register("valid_correct_email@test.com", \
    "valid_correct_password", "valid_correct_first_name", \
    "valid_correct_last_name")
    token1 = user1["token"]

    user2 = auth_register("valid_correct_email@test2.com", \
    "valid_correct_password", "valid_correct_first_name", \
    "valid_correct_last_name")
    token2 = user2["token"]
    userid2 = user2["u_id"]

    #token1 create a channel
    channel = func.channels_create(token1, "TestChannel", True)
    channel_ids = channel["channel_id"]

    #token2 joins the channel token1 made
    func.channel_join(token2, channel_ids)

    #user2 is not the owner, thus trying to removeowner raises an error
    with pytest.raises(ValueError, match=\
    "User id is not an owner of the channel"):
        func.channel_removeowner(token1, channel_ids, userid2)

    #token1 makes token2 the owner
    func.channel_addowner(token1, channel_ids, userid2)

    assert func.channel_removeowner(token1, channel_ids, userid2) == {}

    #if given an invalid channel_id
    with pytest.raises(ValueError, match="Invalid channel_id"):
        func.channel_removeowner(token1, 100, userid2)

def test_channels_list():
    '''
    Function tests for channels_list
    '''

    user1 = auth_register("valid_correct_email@t.com", \
    "valid_correct_password", "valid_correct_first_name",\
     "valid_correct_last_name")
    token1 = user1["token"]

    user2 = auth_register("valid_correct_email@t1.com", \
    "valid_correct_password", "valid_correct_first_name", \
    "valid_correct_last_name")
    token2 = user2["token"]

    #user1 create a channel (123)
    channel = func.channels_create(token1, "TestChannel", True)

    #user2 create a channel (123)
    func.channels_create(token2, "TestChannel2", True)

    assert func.channels_list(token1) == {"id" : "channel_ids",\
     "name" : "TestChannel"}

    assert func.channels_list(token2) == {"id" : "channel_ids2",\
     "name" : "TestChannel2"}

    #user2 creates another channel
    func.channels_create(token2, "TestChannel3", True)

    #assert token2 is in two channels
    assert func.channels_list(token2) == {"id" : "channel_ids2", \
    "name" : "TestChannel2"}, {"id" : "channel_ids3", "name" : "TestChannel3"}

def test_channels_listall():
    '''
    Function tests for channels_listall
    '''

    user1 = auth_register("valid_correct_email@t.com", \
    "valid_correct_password", "valid_correct_first_name", \
    "valid_correct_last_name")
    token1 = user1["token"]

    func.channels_create(token1, "TestChannel1", True)

    assert func.channels_list(token1) == {"id" : "channel_ids",\
     "name" : "TestChannel1"}

    #creating another channel
    func.channels_create(token1, "TestChannel2", False)

    assert func.channels_list(token1) == {"id": "channel_ids", \
    "name" : "TestChannel1"}, {"id": "channel_ids2", "name": "TestChannel2"}

    #if given invalid token
    with pytest.raises(ValueError, match="Invalid token"):
        func.channels_listall("12345")

def test_channels_create():
    '''
    Function tests for channels_create
    '''

    user1 = auth_register("valid_correct_email@t.com", \
    "valid_correct_password", "valid_correct_first_name",\
    "valid_correct_last_name")
    token1 = user1["token"]

    #user1 create a channel
    func.channels_create(user1, "TestChannel", True)

    assert func.channels_create(token1, "Channel1", True) == \
    {"channel_id" : get_channel_id("Channel1")}
    assert func.channels_create(token1, "Channel2", False) == \
    {"channel_id" : get_channel_id("Channel2")}

    #public channel, name longer than 20 characters
    with pytest.raises(ValueError, match=\
    "Name is more than 20 characters long"):
        func.channels_create(token1, "asdbcdjsisjd222isjdisjdisjdis", True)

    #private channel, name longer than 20 characters
    with pytest.raises(ValueError, match=\
    "Name is more than 20 characters long"):
        func.channels_create(token1, "asdbcdjsisjd222isjdisjdis", False)

# helper function to get channel ID from database given the channel name
def get_channel_id(name):
    '''
    helper
    '''
    return 123
