'''
Testing Channel functions Iteration 2
Team: You_Things_Can_Choose
'''

import pytest
import server.global_var as global_var
from server import channel_functions as func
from server.auth_functions import auth_register
from server.Error import AccessError
from server.message_functions import message_send

def test_channel_invite():
    '''
    Testing for inviting a user to a channel
    '''

    #Initialisation
    global_var.initialise_all()

    # Create an user who owns the channel
    user1 = auth_register("test_email@gmail.com", "password123", \
         "Rayden", "Smith")
    token_1 = user1["token"]

    # Create user that is invited to channel
    user2 = auth_register("test_email2@gmail.com", "thisisapassword", \
         "Bob", "Sally")
    token_2 = user2["token"]
    userid_2 = user2["u_id"]

    # Create user that will not be part of channel
    user3 = auth_register("test_email3@gmail.com", "arandompassword", \
         "Coen", "Kevin")
    token_3 = user3["token"]

    # Create a channel
    channel = func.channels_create(token_1, "TestChannel1", True)
    channel_id = channel["channel_id"]
    # Initialisation finished

    # User2 is successfully invited to channel
    assert func.channel_invite(token_1, channel_id, userid_2) == {}

    # If the invite was successful, user2 can send a message
    assert message_send(token_2, channel_id, "A successful message") \
         == {"message_id" : 0}

    # User leaves the channel
    assert func.channel_leave(token_2, channel_id) == {}

    # User is not invited if given an invalid token
    with pytest.raises(AccessError, match="Invalid token"):
        func.channel_invite("12345", channel_id, userid_2)

    # User is not inivited if given an invalid channel_id
    with pytest.raises(ValueError, match="Channel does not exist"):
        func.channel_invite(token_1, 100, userid_2)

    # Inviting user is not apart of the channel
    with pytest.raises(AccessError, \
         match="Authorised user is not a member of the channel"):
        func.channel_invite(token_3, channel_id, userid_2)

    # If user being invited is not an user
    with pytest.raises(ValueError, match="User id is not valid"):
        func.channel_invite(token_1, channel_id, 111111)

def test_channel_details():
    '''
    Function tests for channel_details
    '''
    #initialisation
    global_var.initialise_all()

    user1 = auth_register("valid_correct_email@test.com", \
    "valid_correct_password", "valid_correct_first_name", \
    "valid_correct_last_name")
    token1 = user1["token"]
    userdict1 = {
        "u_id": 0, 
        "name_first": "valid_correct_first_name", 
        "name_last": "valid_correct_last_name"
    }

    user2 = auth_register("valid_correct_email2@test.com", \
    "valid_correct_password", "valid_correct_first_name", \
    "valid_correct_last_name")
    token2 = user2["token"]
    userdict2 = {
        "u_id": 1, 
        "name_first": "valid_correct_first_name", 
        "name_last": "valid_correct_last_name"
    }

    #token1 creates a channel and is automatically part of it as the owner
    channel = func.channels_create(token1, "TestChannel", True)
    channel_id = channel["channel_id"]

    #if user is not a member of the channel, has not joined yet
    with pytest.raises(AccessError, match=\
    "Authorised user is not a member of the channel"):
        func.channel_details(token2, channel_id)

    assert func.channel_details(token1, channel_id) == \
    {"name" : "TestChannel", "owner_members": [userdict1], \
         "all_members": [userdict1]}

    #if given an invalid channel_id
    with pytest.raises(ValueError, match="Channel does not exist"):
        func.channel_details(token1, 100)

    # The function is called using a invalid token
    with pytest.raises(AccessError, match="Invalid token"):
        func.channel_details("12345", channel_id)

    # A second user joins the channel
    func.channel_join(token2, channel_id)

    assert func.channel_details(token1, channel_id) == \
    {"name" : "TestChannel", "owner_members": [userdict1], \
         "all_members": [userdict1, userdict2]}

def test_channel_messages():
    '''
    Function tests for channel_messages
    '''
    #initialisation
    global_var.initialise_all()

    user1 = auth_register("channel_messages@test.com", "password", \
    "channel_messages", "test")
    token1 = user1["token"]

    user2 = auth_register("channel_messages@test2.com", "password", \
    "channel_messages2", "test2")
    token2 = user2["token"]

    #create a channel
    channel = func.channels_create(token1, "TestChannel", True)
    channel_id = channel["channel_id"]

    # Start index is invalid as there are no message
    with pytest.raises(ValueError, match="Start index is invalid"):
        func.channel_messages(token1, channel_id, 1)

    # send a message to the channel and check that return is correct
    message_send(token1, channel_id, '1 message')

    messages = func.channel_messages(token1, channel_id, 0)
    assert messages["start"] == 0
    assert messages["end"] == -1
    assert messages["messages"][0]["message_id"] == 0
    assert messages["messages"][0]["u_id"] == user1["u_id"]
    assert messages["messages"][0]["message"] == "1 message"

    # send a message to the channel and check that return is correct
    message_send(token1, channel_id, '2 message')

    messages = func.channel_messages(token1, channel_id, 0)
    assert messages["messages"][0]["message"] == "2 message"
    assert messages["messages"][1]["message"] == "1 message"

    for i in range(3, 51):
        message_send(token1, channel_id, f'{i} message')

    # A total of 50 messages are sent
    messages = func.channel_messages(token1, channel_id, 0)
    assert messages["start"] == 0
    assert messages["end"] == 49
    assert messages["messages"][0]["message"] == "50 message"
    assert messages["messages"][49]["message"] == "1 message"

    messages = func.channel_messages(token1, channel_id, 1)
    assert messages["start"] == 1
    assert messages["end"] == -1
    assert messages["messages"][0]["message"] == "49 message"
    assert messages["messages"][48]["message"] == "1 message"

    # test exceptions
    with pytest.raises(ValueError, match="Channel does not exist"):
        func.channel_messages(token1, -1, 0)

    # The function is called using a invalid token
    with pytest.raises(AccessError, match="Invalid token"):
        func.channel_messages("12345", channel_id, 0)

    with pytest.raises(ValueError, match="Start index is invalid"):
        func.channel_messages(token1, channel_id, 100)

    with pytest.raises(AccessError, match=\
    "Authorised user is not a member of the channel"):
        func.channel_messages(token2, channel_id, 0)

def test_channel_leave():
    '''
    Function tests for channel_leave
    '''
    #initialisation
    global_var.initialise_all()

    user1 = auth_register("valid_correct_email@test.com", \
    "valid_correct_password", "valid_correct_first_name", \
    "valid_correct_last_name")
    token1 = user1["token"]

    #create a channel
    channel = func.channels_create(token1, "TestChannel", True)
    channel_id = channel["channel_id"]

    # The function is called using a invalid token
    with pytest.raises(AccessError, match="Invalid token"):
        func.channel_leave("12345", channel_id)

    # User is in channel so can send message
    message_send(token1, channel_id, "can send message")

    assert func.channel_leave(token1, channel_id) == {}

    # user has left channel and so can't send messages
    with pytest.raises(AccessError, \
         match="Authorised user is not a member of the channel"):
        message_send(token1, channel_id, "can't send message")

    #if given an invalid channel_id
    with pytest.raises(ValueError, match="Channel does not exist"):
        func.channel_leave(token1, 100)

    # User is already removed, but will not cause Error
    assert func.channel_leave(token1, channel_id) == {}

def test_channel_join():
    '''
    Function tests for channel_join
    '''
    #initialisation
    global_var.initialise_all()

    user1 = auth_register("valid_correct_email@test.com", \
    "valid_correct_password", "valid_correct_first_name",\
     "valid_correct_last_name")
    token1 = user1["token"]

    user2 = auth_register("valid_correct_email@test2.com", \
    "valid_correct_password", "valid_correct_first_name", \
    "valid_correct_last_name")
    token2 = user2["token"]

    #user 2 create a channel
    channel = func.channels_create(token1, "PublicChannel", True)
    channel_ids = channel["channel_id"]

    #user 2 create a private channel
    channel2 = func.channels_create(token1, "PrivateChannel", False)
    channel_private = channel2["channel_id"]

    assert func.channel_join(token2, channel_ids) == {}

    #if given an invalid channel_id
    with pytest.raises(ValueError, match="Channel does not exist"):
        func.channel_join(token1, 100)

    #if channel is private and user is not the admin
    with pytest.raises(AccessError, match=\
    "Channel is private and user is not admin"):
        func.channel_join(token2, channel_private)

    # A slackr owner leaves a private channel and can join back in
    func.channel_leave(token1, channel_ids)
    func.channel_join(token1, channel_ids)


def test_channel_addowner():
    '''
    Function tests for channel_addowner
    '''
    global_var.initialise_all()

    owner = auth_register("valid_correct_email@test.com", \
    "valid_correct_password", "valid_correct_first_name", \
    "valid_correct_last_name")
    token_owner = owner["token"]

    user1 = auth_register("valid_correct_email@test1.com", \
    "valid_correct_password", "valid_correct_first_name",\
     "valid_correct_last_name")
    token1 = user1["token"]
    userid1 = user1["u_id"]

    user2 = auth_register("valid_correct_email@test2.com",\
     "valid_correct_password", "valid_correct_first_name", \
     "valid_correct_last_name")
    userid2 = user2["u_id"]
    token2 = user2["token"]

    #owner creates a channel and is automatically the owner
    channel = func.channels_create(token_owner, "TestChannel", True)
    channel_id = channel["channel_id"]

    #if given an invalid channel_id
    with pytest.raises(ValueError, match="Channel does not exist"):
        func.channel_addowner(token_owner, 100, userid1)

    #token 1&2 joins channel that owner created
    func.channel_join(token1, channel_id)
    func.channel_join(token2, channel_id)

    #token1 is not an owner of the channel
    with pytest.raises(AccessError, match=\
    "User is not an owner of the channel"):
        func.channel_addowner(token1, channel_id, userid2)

    # owner successfully promotes user to owner
    assert func.channel_addowner(token_owner, channel_id, userid1) == {}

    # user 1 can now promote other to owner
    assert func.channel_addowner(token1, channel_id, userid2) == {}

    #token1/userid1 is already an owner of the channel
    with pytest.raises(ValueError, match=\
    "User is already an owner of the channel"):
        func.channel_addowner(token_owner, channel_id, userid1)

def test_channel_removeowner():
    '''
    Function tests for channel_removeowner
    '''
    global_var.initialise_all()

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
    channel_id = channel["channel_id"]

    #token2 joins the channel token1 made
    func.channel_join(token2, channel_id)

    #user2 is not the owner, thus trying to removeowner raises an error
    with pytest.raises(ValueError, match=\
    "User id is not an owner of the channel"):
        func.channel_removeowner(token1, channel_id, userid2)

    #token1 makes token2 the owner
    func.channel_addowner(token1, channel_id, userid2)

    assert func.channel_removeowner(token1, channel_id, userid2) == {}

    #if given an invalid channel_id
    with pytest.raises(ValueError, match="Channel does not exist"):
        func.channel_removeowner(token1, 100, userid2)

def test_channels_list():
    '''
    Function tests for channels_list
    '''
    global_var.initialise_all()

    user1 = auth_register("valid_correct_email@t.com", \
    "valid_correct_password", "valid_correct_first_name",\
     "valid_correct_last_name")
    token1 = user1["token"]

    user2 = auth_register("valid_correct_email@t1.com", \
    "valid_correct_password", "valid_correct_first_name", \
    "valid_correct_last_name")
    token2 = user2["token"]

    assert func.channels_list(token1) == {"channels": []}

    #user1 create a channel
    func.channels_create(token1, "TestChannel", True)

    #user2 create a channel
    func.channels_create(token2, "TestChannel2", True)

    assert func.channels_list(token1) == {"channels": [{"channel_id" : 0,\
     "name" : "TestChannel"}]}

    assert func.channels_list(token2) == {"channels": [{"channel_id" : 1,\
     "name" : "TestChannel2"}]}

    #user2 creates another channel
    func.channels_create(token2, "TestChannel3", True)

    #assert token2 is in two channels
    assert func.channels_list(token2) == {"channels" :[{"channel_id" : 1, \
    "name" : "TestChannel2"}, {"channel_id" : 2, "name" : "TestChannel3"}]}

def test_channels_listall():
    '''
    Function tests for channels_listall
    '''
    global_var.initialise_all()

    user1 = auth_register("valid_correct_email@t.com", \
    "valid_correct_password", "valid_correct_first_name", \
    "valid_correct_last_name")
    token1 = user1["token"]

    user2 = auth_register("valid_correct_email@t1.com", \
    "valid_correct_password", "valid_correct_first_name", \
    "valid_correct_last_name")
    token2 = user2["token"]

    assert func.channels_listall(token1) == {"channels": []}

     #if given invalid token
    with pytest.raises(AccessError, match="Invalid token"):
        func.channels_listall("12345")

    func.channels_create(token1, "TestChannel1", True)

    assert func.channels_listall(token1) == {"channels": [{"channel_id" : 0,\
     "name" : "TestChannel1"}]}

    #creating another channel
    func.channels_create(token1, "TestChannel2", False)

    assert func.channels_listall(token1) == {"channels" :[{"channel_id" : 0, \
    "name" : "TestChannel1"}, {"channel_id" : 1, "name" : "TestChannel2"}]}

    # user 2 creates a channel
    func.channels_create(token2, "TestChannel3", True)

    # displays channels the user is not apart of
    assert func.channels_listall(token1) == {"channels" :[{"channel_id" : 0, \
    "name" : "TestChannel1"}, {"channel_id" : 1, "name" : "TestChannel2"}, \
        {"channel_id": 2, "name": "TestChannel3"}]}


def test_channels_create():
    '''
    Function tests for channels_create
    '''
    global_var.initialise_all()

    user1 = auth_register("valid_correct_email@t.com", \
    "valid_correct_password", "valid_correct_first_name",\
    "valid_correct_last_name")
    token1 = user1["token"]

    #user1 create a channel
    func.channels_create(token1, "TestChannel", True)

    assert func.channels_create(token1, "Channel1", True) == \
    {"channel_id" : 1}
    assert func.channels_create(token1, "Channel2", False) == \
    {"channel_id" : 2}

    #public channel, name longer than 20 characters
    with pytest.raises(ValueError, match=\
    "Name is longer than 20 characters"):
        func.channels_create(token1, "a" * 21, True)

    #private channel, name longer than 20 characters
    with pytest.raises(ValueError, match=\
    "Name is longer than 20 characters"):
        func.channels_create(token1, "a" * 21, False)
