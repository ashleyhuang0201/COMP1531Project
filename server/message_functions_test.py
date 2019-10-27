'''
Testing message functions Iteration 2
Team: You_Things_Can_Choose
'''

#Import functions for testing
import datetime
import pytest
import server.global_var as global_var
from server import helpers
from server import message_functions as funcs
from server import auth_functions
from server import channel_functions
from server.Error import AccessError

def test_message_sendlater():
    '''
    Function tests for message_sendlater
    '''

    #Initialisation
    global_var.initialise_all()
    assert global_var.data["users"] == []

    #Create a user
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
         "Rayden", "Smith")
    assert global_var.data["users"] != []
    token = user["token"]

    #User creates a channel
    channel = channel_functions.channels_create(token, "ChannelName", True)
    channel_id = channel["channel_id"]
    #Init finished

    #User sends message to created channel
    assert funcs.message_sendlater(token, channel_id, \
            "This is a valid message", datetime.datetime(2020, 1, 1).timestamp())  \
                                                        == {"message_id": 0}

    #Sending a message of length 1000 is valid
    assert funcs.message_sendlater(token, channel_id, create_long_string(), \
         datetime.datetime(2020, 1, 1).timestamp()) == {"message_id": 1}

    #A message of length greater than 1000 is valid
    with pytest.raises(ValueError, match="Message length too long"):
        funcs.message_sendlater(token, channel_id, "1" + create_long_string(), \
             datetime.datetime(2020, 1, 1).timestamp())

    #An exception is thrown if a invalid token is given
    with pytest.raises(AccessError, match="Invalid token"):
        funcs.message_sendlater("111111", channel_id, \
             "This is a valid message", datetime.datetime(2020, 1, 1).timestamp())

    #The channel based on ID does not exist
    with pytest.raises(ValueError, match="Invalid Channel ID"):
        funcs.message_sendlater(token, 99, "This is a valid message", \
             datetime.datetime(2020, 1, 1).timestamp())

    #Time sent is a time in the past
    with pytest.raises(ValueError, match="Time sent was in the past"):
        funcs.message_sendlater(token, channel_id, "This is a valid message", \
             datetime.datetime(2019, 1, 1).timestamp())

    #All errors (Token error is caught first)
    with pytest.raises(AccessError, match="Invalid token"):
        funcs.message_sendlater("111111", 99, "1" + create_long_string(), \
             datetime.datetime(2019, 1, 1).timestamp())

    #User leaves channel
    channel_functions.channel_leave(token, channel_id)

    #User cannot send message to channel he is not apart of
    with pytest.raises(AccessError, \
         match="Authorised user is not a member of the channel"):
        funcs.message_sendlater(token, channel_id, "This is a valid message", \
             datetime.datetime(2020, 1, 1).timestamp())


def test_message_send():
    '''
    Function tests for message_send
    '''

    #Initialisation
    global_var.initialise_all()
    assert global_var.data["users"] == []

    #Creates an user
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
            "Rayden", "Smith")
    assert user == {"u_id": 0, "token": helpers.encode_token_for_u_id(0)}
    token = user["token"]
    assert global_var.data["users"] != []

    #User creates a channel
    channel = channel_functions.channels_create(token, "ChannelName", True)
    assert channel == {"channel_id": 0}
    channel_id = channel["channel_id"]
    #Initialisation finished

    #User successfully sends message to created channel
    assert funcs.message_send(token, channel_id, \
                            "This is a valid message") == {"message_id": 0}

    #A invalid token is sent to the function
    with pytest.raises(AccessError, match="Invalid token"):
        funcs.message_send("111111", channel_id, "This is a valid message")

    #The channel based on ID does not exist
    with pytest.raises(ValueError, match="Invalid Channel ID"):
        funcs.message_send(token, 99, "This is a valid message")

    #Sending a message of length 1000 is valid
    assert funcs.message_send(token, channel_id, create_long_string()) \
                            == {"message_id" : 1}

    #A message of length greater than 1000
    with pytest.raises(ValueError, match="Message length too long"):
        funcs.message_send(token, channel_id, "1" + create_long_string())

    #Thrown multiple errors, token error is caught first
    with pytest.raises(AccessError, match="Invalid token"):
        funcs.message_send("111111", 99, "1" + create_long_string())

    #User leaves channel
    channel_functions.channel_leave(token, channel_id)

    #User cannot send message to channel he is not apart of
    with pytest.raises(AccessError, \
            match="Authorised user is not a member of the channel"):
        funcs.message_send(token, channel_id, "This is a valid message")


def test_message_remove():
    '''
    Function tests for message_remove
    '''

    #Initialisation
    global_var.initialise_all()
    assert global_var.data["users"] == []
    #Create users
    owner = auth_functions.auth_register("test2@gmail.com", "pass123", \
         "Sally", "Bob")
    owner_token = owner["token"]

    user = auth_functions.auth_register("test@gmail.com", "pass123", \
         "Rayden", "Smith")
    token = user["token"]
    assert global_var.data["users"] != []

    #owner creates a channel and so is the owner
    channel = channel_functions.channels_create(owner_token, "Name", True)
    assert channel == {"channel_id" : 0}
    channel_id = channel["channel_id"]

    #user joins the channel
    channel_functions.channel_join(token, channel_id)

    #3 messages are sent
    assert funcs.message_send(token, channel_id, "This is a valid message") \
         == {"message_id" : 0}
    assert funcs.message_send(token, channel_id, \
         "This is another valid message") == {"message_id" : 1}
    assert funcs.message_send(owner_token, channel_id, \
         "This is not your message") == {"message_id" : 2}
    #Initialisation finished


    #A invalid token is sent to the function
    with pytest.raises(AccessError, match="Invalid token"):
        funcs.message_remove("111111", 0)

    #owner successfully removes a message
    assert funcs.message_remove(owner_token, 0) == {}

    # As message was removed, it can not be removed again
    with pytest.raises(ValueError, match="Message does not exist"):
        funcs.message_remove(owner_token, 0)

    #user successfully removes his own message
    assert funcs.message_remove(token, 1) == {}

    #A owner tries to remove a invalid message based on message_id
    with pytest.raises(ValueError, match="Message does not exist"):
        funcs.message_remove(owner_token, 99)

    #A user tries to remove a invalid message based on message_id
    with pytest.raises(ValueError, match="Message does not exist"):
        funcs.message_remove(token, 99)

    #user is unable to remove a message not his/her's
    with pytest.raises(AccessError, match="User does not have permission"):
        funcs.message_remove(token, 2)


def test_message_edit():
    '''
    Function tests for message_edit
    '''
    #Initialisation
    global_var.initialise_all()

    #Create users
    owner = auth_functions.auth_register("test2@gmail.com", "pass123", \
         "Sally", "Bob")
    owner_token = owner["token"]

    user = auth_functions.auth_register("test@gmail.com", "pass123", \
         "Rayden", "Smith")
    token = user["token"]

    #owner creates a channel and so is the owner
    channel = channel_functions.channels_create(owner_token, "Name", True)
    channel_id = channel["channel_id"]

    #user joins the channel
    channel_functions.channel_join(token, channel_id)

    #3 messages are sent
    assert funcs.message_send(token, channel_id, "This is a valid message") \
         == {"message_id" : 0}
    assert funcs.message_send(token, channel_id, \
         "This is another valid message") == {"message_id" : 1}
    assert funcs.message_send(owner_token, channel_id, \
         "This is not your message") == {"message_id" : 2}
    #Init finished

    #A owner edits a message
    assert funcs.message_edit(owner_token, 0, "This is a valid edit") == {}

    #A user edits his own message
    assert funcs.message_edit(token, 1, "This is another valid edit") == {}

    #A invalid token is sent to the function
    with pytest.raises(AccessError, match="Invalid token"):
        funcs.message_edit("111111", 0, "This is a valid edit")

    #A owner tries to edit a invalid message based on message_id
    with pytest.raises(ValueError, match="Message does not exist"):
        funcs.message_edit(owner_token, 99, "This is a valid edit")

    #A user tries to edit a invalid message based on message_id
    with pytest.raises(ValueError, match="Message does not exist"):
        funcs.message_edit(token, 99, "A valid message edit")

    #A user tries to edit a message not his
    with pytest.raises(AccessError, match="User does not have permission"):
        funcs.message_edit(token, 2, "This is a valid message")

    #The edited message was too long
    with pytest.raises(ValueError, match="Message length too long"):
        funcs.message_edit(owner_token, 0, "1" + create_long_string())


def test_message_react():
    '''
    Function tests for message_react
    '''
    #Initialisation
    global_var.initialise_all()

    user = auth_functions.auth_register("test@gmail.com", "pass123", \
         "Rayden", "Smith")
    token = user["token"]

    user_2 = auth_functions.auth_register("test2@gmail.com", "password", \
        "Bob", "Sally")
    token_2 = user_2["token"]

    #User creates a channel
    channel = channel_functions.channels_create(token, "Name", True)
    channel_id = channel["channel_id"]

    channel_functions.channel_join(token_2, channel_id)

    #user sends 3 messages
    assert funcs.message_send(token, channel_id, "This is a valid message") \
         == {"message_id" : 0}
    assert funcs.message_send(token, channel_id, \
         "This is another valid message") == {"message_id" : 1}
    assert funcs.message_send(token, channel_id, \
         "This is your message") == {"message_id" : 2}
    #Initialisation finished

    #An invalid token is sent to the function
    with pytest.raises(AccessError, match="Invalid token"):
        funcs.message_react("111111", 0, 1)

    #An user successfully reacts
    assert funcs.message_react(token, 0, 1) == {}

    #Another user also reacts to the same message
    assert funcs.message_react(token_2, 0, 1) == {}

    #An user tries to react to a invalid message based on message_id
    with pytest.raises(ValueError, match="Message does not exist"):
        funcs.message_react(token, 99, 1)

    #An user tries to react to a message already reacted to
    with pytest.raises(ValueError, match="Message contains an active react"):
        funcs.message_react(token, 0, 1)

    #An user uses a invalid react id
    with pytest.raises(ValueError, match="Invalid React ID"):
        funcs.message_react(token, 1, 99)

# message_unreact(token, message_id, react_id)
def test_message_unreact():
    '''
    Funtion tests for message_uncreat
    '''
    #Initialisation
    global_var.initialise_all()

    user = auth_functions.auth_register("test@gmail.com", "pass123", \
         "Rayden", "Smith")
    token = user["token"]

    #User creates a channel
    channel = channel_functions.channels_create(token, "Name", True)
    channel_id = channel["channel_id"]

    #user sends 3 messages
    assert funcs.message_send(token, channel_id, "This is a valid message") \
         == {"message_id" : 0}
    assert funcs.message_send(token, channel_id, \
         "This is another valid message") == {"message_id" : 1}
    assert funcs.message_send(token, channel_id, \
         "This is not your message") == {"message_id" : 2}
    #Init finished

    # A message is reacted to
    funcs.message_react(token, 0, 1)

    #A invalid token is sent to the function
    # (A invalid user is trying to use the function)
    with pytest.raises(AccessError, match="Invalid token"):
        funcs.message_unreact("111111", 0, 1)

    #A user successfully unreacts
    assert funcs.message_unreact(token, 0, 1) == {}

    #A user tries to unreact to a invalid message based on message_id
    with pytest.raises(ValueError, match="Message does not exist"):
        funcs.message_unreact(token, 99, 1)

    #A user tries to unreact to a message that is not reacted to
    with pytest.raises(ValueError, match=\
         "Message does not contain an active react"):
        funcs.message_unreact(token, 1, 1)

    # message is reacted to again
    funcs.message_react(token, 0, 1)
    #A user uses a invalid unreact id
    with pytest.raises(ValueError, match="Invalid React ID"):
        funcs.message_unreact(token, 0, 99)

# message_pin(token, message_id)
def test_message_pin():
    '''
    Function tests for message_pin
    '''
    #Initialisation
    global_var.initialise_all()

    #Create users
    owner = auth_functions.auth_register("test2@gmail.com", "pass123", \
         "Sally", "Bob")
    assert owner == {"u_id": 0, "token": helpers.encode_token_for_u_id(0)}
    owner_token = owner["token"]

    user = auth_functions.auth_register("test@gmail.com", "pass123", \
         "Rayden", "Smith")
    token = user["token"]

    #owner that creates the channel and so is the owner
    channel = channel_functions.channels_create(owner_token, "Name", True)
    channel_id = channel["channel_id"]

    #user joins the channel
    channel_functions.channel_join(token, channel_id)

    #user sends 3 messages
    assert funcs.message_send(token, channel_id, "This is a valid message") \
         == {"message_id" : 0}
    assert funcs.message_send(token, channel_id, \
         "This is another valid message") == {"message_id" : 1}
    assert funcs.message_send(owner_token, channel_id, \
         "This is not your message") == {"message_id" : 2}
    #Init finished

    #A invalid token is sent to the function
    # (A invalid user is trying to use the function)
    with pytest.raises(AccessError, match="Invalid token"):
        funcs.message_pin("111111", 0)

    #A user is not an admin
    with pytest.raises(ValueError, match="User is not an admin"):
        funcs.message_pin(token, 0)

    #A admin user successfully pins a message
    assert funcs.message_pin(owner_token, 0) == {}

    #Message is invalid based on message_id
    with pytest.raises(ValueError, match="Message does not exist"):
        funcs.message_pin(owner_token, 99)

    #Message is already pinned
    with pytest.raises(ValueError, match="Message is currently pinned"):
        funcs.message_pin(owner_token, 0)

    #Admin leaves channel
    channel_functions.channel_leave(owner_token, channel_id)

    #Admin is not a member of the channel
    with pytest.raises(AccessError, match=\
         "Authorised user is not a member of the channel"):
        funcs.message_pin(owner_token, 1)

# message_unpin(token, message_id)
def test_message_unpin():
    '''
    Function tests for message_unpin
    '''
    #Initialisation
    global_var.initialise_all()

    #Create users
    owner = auth_functions.auth_register("test2@gmail.com", "pass123", \
         "Sally", "Bob")
    owner_token = owner["token"]

    user = auth_functions.auth_register("test@gmail.com", "pass123", \
         "Rayden", "Smith")
    token = user["token"]

    #owner that creates the channel and so is the owner
    channel = channel_functions.channels_create(owner_token, "Name", True)
    channel_id = channel["channel_id"]

    #user joins the channel
    channel_functions.channel_join(token, channel_id)

    #user sends 3 messages
    assert funcs.message_send(token, channel_id, "This is a valid message") \
         == {"message_id" : 0}
    assert funcs.message_send(token, channel_id, \
         "This is another valid message") == {"message_id" : 1}
    assert funcs.message_send(owner_token, channel_id, \
         "This is not your message") == {"message_id" : 2}
    #Init finished

    # A message is pinned
    assert funcs.message_pin(owner_token, 0) == {}

    #A user is not an admin
    with pytest.raises(ValueError, match="User is not an admin"):
        funcs.message_unpin(token, 0)

    #A user successfully unpins a message
    assert funcs.message_unpin(owner_token, 0) == {}

    #Message is already unpinned
    with pytest.raises(ValueError, match="Message is currently unpinned"):
        funcs.message_unpin(owner_token, 0)

    # Message can be pinned after being unpinned
    assert funcs.message_pin(owner_token, 0) == {}

    #Message is invalid based on message_id
    with pytest.raises(ValueError, match="Message does not exist"):
        funcs.message_unpin(owner_token, 99)

    assert funcs.message_pin(owner_token, 1) == {}

    #Admin leaves channel
    channel_functions.channel_leave(owner_token, channel_id)

    #Admin is not a member of the channel
    with pytest.raises(AccessError, match=\
         "Authorised user is not a member of the channel"):
        funcs.message_unpin(owner_token, 1)

#Helper Functions
#Creates a string of 1000 characters for testing purposes
def create_long_string():
    '''
    Helper
    '''
    longstring = ""
    for _ in range(1000):
        longstring += "a"
    assert len(longstring) == 1000

    return longstring
