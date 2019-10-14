'''
Functions for testing message_* functions
Created by: Michael Zhang
Created on: 29/9/2019
'''

#Import functions for testing
import datetime
import pytest
from server.message import message_functions as funcs
from server.auth import auth_functions
from server.channel import channel_functions
from server.search import search_function
from server.helper.Error import AccessError

# message_sendlater(token, channel_id, message, time_sent)
def test_message_sendlater():
    '''
    Function tests for message_sendlater
    '''
    #Initialisation
    #Create a user
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
         "Rayden", "Smith")

    token = user["token"]
    #User creates a channel
    channel = channel_functions.channels_create(token, "Name", True)
    #Init finished

    #User sends message to created channel
    assert funcs.message_sendlater(token, channel, "This is a valid message", \
         datetime.datetime(2020, 1, 1)) == {}

    #Sending a message of length 1000 is valid
    assert funcs.message_sendlater(token, channel, create_long_string(), \
         datetime.datetime(2020, 1, 1)) == {}

    #A message of length greater than 1000 is valid
    with pytest.raises(ValueError, match="Message length too long"):
        funcs.message_sendlater(token, channel, "1" + create_long_string(), \
             datetime.datetime(2020, 1, 1))

    #An exception is thrown if a invalid token is given
    with pytest.raises(ValueError, match="Invalid Token"):
        funcs.message_sendlater("111111", channel, "This is a valid message", \
             datetime.datetime(2020, 1, 1))

    #The channel based on ID does not exist
    with pytest.raises(ValueError, match="Invalid Channel ID"):
        funcs.message_sendlater(token, 99, "This is a valid message", \
             datetime.datetime(2020, 1, 1))

    #Time sent is a time in the past
    with pytest.raises(ValueError, match="Time sent was in the past"):
        funcs.message_sendlater(token, channel, "This is a valid message", \
             datetime.datetime(2019, 1, 1))

    #All errors (Token error is caught first)
    with pytest.raises(ValueError, match="Invalid Token"):
        funcs.message_sendlater("111111", 99, "1" + create_long_string(), \
             datetime.datetime(2019, 1, 1))

    #User leaves channel
    channel_functions.channel_leave(token, channel)

    #User cannot send message to channel he is not apart of
    with pytest.raises(ValueError, match="User not member of channel"):
        funcs.message_sendlater(token, channel, "This is a valid message", \
             datetime.datetime(2020, 1, 1))

# message_send(token, channel_id, message)
def test_message_send():
    '''
    Function tests for message_send
    '''
    #Initialisation
    #Create an user
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
            "Rayden", "Smith")

    token = user["token"]
    #User creates a channel
    channel = channel_functions.channels_create(token, "Name", True)
    #Init finished

    #User sends message to created channel
    assert funcs.message_send(token, channel, "This is a valid message") == {}

    #Sending a message of length 1000 is valid
    assert funcs.message_send(token, channel, create_long_string()) == {}

    #A invalid token is sent to the function
    # (A invalid user is trying to use the function)
    with pytest.raises(ValueError, match="Invalid Token"):
        funcs.message_send("111111", channel, "This is a valid message")

    #The channel based on ID does not exist
    with pytest.raises(ValueError, match="Invalid Channel ID"):
        funcs.message_send(token, 99, "This is a valid message")

    #A message of length greater than 1000
    with pytest.raises(ValueError, match="Message length too long"):
        funcs.message_send(token, channel, "1" + create_long_string())

    #All errors (Token error is caught first)
    with pytest.raises(ValueError, match="Invalid Token"):
        funcs.message_send("111111", 99, "1" + create_long_string())

    #User leaves channel
    channel_functions.channel_leave(token, channel)

    #User cannot send message to channel he is not apart of
    with pytest.raises(ValueError, match="User not member of channel"):
        funcs.message_send(token, channel, "This is a valid message")

# message_remove(token, message_id)
def test_message_remove():
    '''
    Function tests for message_remove
    '''
    #Initialisation
    #Create users
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
         "Rayden", "Smith")
    token = user["token"]

    owner = auth_functions.auth_register("test2@gmail.com", "pass123", \
         "Sally", "Bob")
    owner_token = owner["token"]

    #owner that creates the channel and so is the owner
    channel = channel_functions.channels_create(owner_token, "Name", True)

    #user joins the channel
    channel_functions.channel_join(token, channel)

    #user sends 3 messages
    funcs.message_send(token, channel, "This is a valid message")
    funcs.message_send(token, channel, "This is another valid message")
    funcs.message_send(owner_token, channel, "This is not your message")
    #Init finished

    #Gets message_id of "This is a valid message"
    message_id = search_function.search(token, \
        "This is a valid message")[0]['messages_id']

    #owner successfully removes a message
    assert funcs.message_remove(owner_token, message_id) == {}

    #Gets message_id of "This is another valid message"
    message_id = search_function.search(token, \
        "This is another valid message")[0]['messages_id']

    #user successfully removes his own message
    assert funcs.message_remove(token, message_id) == {}

    #A owner tries to remove a invalid message based on message_id
    with pytest.raises(ValueError, match="Invalid Message ID"):
        funcs.message_remove("owner", 99)

    #A user tries to remove a invalid message based on message_id
    with pytest.raises(ValueError, match="Invalid Message ID"):
        funcs.message_remove(token, 99)

    #Gets message_id of "This is another valid message"
    message_id = search_function.search(token, \
        "This is not your message")[0]['messages_id']

    #user is unable to remove a message not his/her's
    with pytest.raises(AccessError, match="User does not have permission"):
        funcs.message_remove(token, message_id)

# message_edit(token, message_id, message)
def test_message_edit():
    '''
    Function tests for message_edit
    '''
    #Initialisation
    #Create users
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
         "Rayden", "Smith")
    token = user["token"]

    owner = auth_functions.auth_register("test2@gmail.com", "pass123", \
         "Sally", "Bob")
    owner_token = owner["token"]

    #owner that creates the channel and so is the owner
    channel = channel_functions.channels_create(owner_token, "Name", True)

    #user joins the channel
    channel_functions.channel_join(token, channel)

    #user sends 3 messages
    funcs.message_send(token, channel, "This is a valid message")
    funcs.message_send(token, channel, "This is another valid message")
    funcs.message_send(owner_token, channel, "This is not your message")
    #Init finished

    #Gets message_id of "This is a valid message"
    message_id = search_function.search(token, \
        "This is a valid message")[0]['messages_id']

    #A owner edits a message
    assert funcs.message_edit(owner_token, message_id, "This is a valid edit") \
         == {}
    #Gets message_id of "This is another valid message"

    #Gets message_id of "This is another valid message"
    message_id = search_function.search(token, \
        "This is another valid message")[0]['messages_id']

    #A user edits his own message
    assert funcs.message_edit(token, message_id, "This is another valid edit") \
         == {}

    #A owner tries to edit a invalid message based on message_id
    with pytest.raises(ValueError, match="Invalid Message ID"):
        funcs.message_edit("owner", 99, "This is a valid message")

    #A user tries to edit a invalid message based on message_id
    with pytest.raises(ValueError, match="Invalid Message ID"):
        funcs.message_edit(token, 99, "This is a valid message")

    #Gets message_id of "This is not your message"
    message_id = search_function.search(token, \
        "This is not your message")[0]['messages_id']

    #A user tries to edit a message not his
    with pytest.raises(AccessError, match="User does not have permission"):
        funcs.message_edit(token, message_id, "This is a valid message")

    #The edited message was too long
    with pytest.raises(ValueError, match="Message length too long"):
        funcs.message_edit("owner", message_id, "1" + create_long_string())

# message_react(token, message_id, react_id)
def test_message_react():
    '''
    Function tests for message_react
    '''
    #Initialisation
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
         "Rayden", "Smith")
    token = user["token"]
    #User creates a channel
    channel = channel_functions.channels_create(token, "Name", True)

    funcs.message_send(token, channel, "This is a valid message")
    funcs.message_send(token, channel, "This is another valid message")
    funcs.message_send(token, channel, "This is a third message")
    #Init finished

    #Gets message_id of "This is a valid message"
    message_id = search_function.search(token, \
        "This is a valid message")[0]['messages_id']

    #A user successfully reacts
    assert funcs.message_react(token, message_id, 1) == {}

    #A user tries to react to a invalid message based on message_id
    with pytest.raises(ValueError, match="Invalid Message ID"):
        funcs.message_react("owner", 99, 1)

    #A user tries to react to a message already reacted to
    with pytest.raises(ValueError, match="Message contains an active react"):
        funcs.message_react(token, message_id, 1)

    #Gets message_id of "This is another valid message"
    message_id = search_function.search(token, \
        "This is another valid message")[0]['messages_id']

    #A user uses a invalid react id
    with pytest.raises(ValueError, match="Invalid React ID"):
        funcs.message_react(token, message_id, 99)

# message_unreact(token, message_id, react_id)
def test_message_unreact():
    '''
    Funtion tests for message_uncreat
    '''
    #Initialisation
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
         "Rayden", "Smith")
    token = user["token"]

    #User creates a channel
    channel = channel_functions.channels_create(token, "Name", True)

    funcs.message_send(token, channel, "This is a valid message")
    funcs.message_send(token, channel, "This is another valid message")
    funcs.message_send(token, channel, "This is a third message")
    #Init finished

    # A message is reacted to
    message_id = search_function.search(token, \
        "This is a valid message")['messages']

    funcs.message_react(token, message_id, 1)

    #A user successfully unreacts
    assert funcs.message_unreact(token, message_id, 1) == {}

    #A user tries to unreact to a invalid message based on message_id
    with pytest.raises(ValueError, match="Invalid Message ID"):
        funcs.message_unreact("owner", 99, 1)

    #A user tries to unreact to a message that is not reacted to
    with pytest.raises(ValueError, match=\
         "Message does not contains an active react"):
        funcs.message_unreact(token, message_id, 1)

    # message is reacted to again
    funcs.message_react(token, message_id, 1)
    #A user uses a invalid react id
    with pytest.raises(ValueError, match="Invalid React ID"):
        funcs.message_unreact(token, 1, 99)

# message_pin(token, message_id)
def test_message_pin():
    '''
    Function tests for message_pin
    '''
    #Initialisation
    #Create users
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
         "Rayden", "Smith")
    token = user["token"]

    owner = auth_functions.auth_register("test2@gmail.com", "pass123", \
         "Sally", "Bob")
    owner_token = owner["token"]

    #owner that creates the channel and so is the owner
    channel = channel_functions.channels_create(owner_token, "Name", True)

    #user joins the channel
    channel_functions.channel_join(token, channel)

    #user sends 3 messages
    funcs.message_send(token, channel, "This is a valid message")
    funcs.message_send(token, channel, "This is another valid message")
    funcs.message_send(owner_token, channel, "This is not your message")
    #Init finished

    #Gets message_id of "This is a valid message"
    message_id = search_function.search(token, \
        "This is a valid message")[0]['messages_id']

    #A user is not an admin
    with pytest.raises(ValueError, match="Not an admin"):
        funcs.message_pin(token, message_id)

    #A admin user successfully pins a message
    assert funcs.message_pin(owner_token, message_id) == {}

    #Message is invalid based on message_id
    with pytest.raises(ValueError, match="Invalid Message ID"):
        funcs.message_pin(owner_token, 99)

    #Message is already pinned
    with pytest.raises(ValueError, match="Message is already pinned"):
        funcs.message_pin(owner_token, message_id)

    #Admin leaves channel
    channel_functions.channel_leave(owner_token, channel)

    #Gets message_id of "This is another valid message"
    message_id = search_function.search(token, \
        "This is another valid message")[0]['messages_id']

    #Admin is not a member of the channel
    with pytest.raises(AccessError, match=\
         "User is not a member of the channel"):
        funcs.message_pin(owner_token, message_id)

# message_unpin(token, message_id)
def test_message_unpin():
    '''
    Function tests for message_unpin
    '''
    #Initialisation
    #Create users
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
         "Rayden", "Smith")
    token = user["token"]

    owner = auth_functions.auth_register("test2@gmail.com", "pass123", \
         "Sally", "Bob")
    owner_token = owner["token"]

    #owner that creates the channel and so is the owner
    channel = channel_functions.channels_create(owner_token, "Name", True)

    #user joins the channel
    channel_functions.channel_join(token, channel)

    #user sends 3 messages
    funcs.message_send(token, channel, "This is a valid message")
    funcs.message_send(token, channel, "This is another valid message")
    funcs.message_send(owner_token, channel, "This is not your message")
    #Init finished

    #Gets message_id of "This is a valid message"
    message_id = search_function.search(token, \
        "This is a valid message")[0]['messages_id']

    #A user is not an admin
    with pytest.raises(ValueError, match="Not an admin"):
        funcs.message_unpin(token, message_id)

    #A user successfully unpins a message
    assert funcs.message_unpin(owner_token, message_id) == {}

    #Message is invalid based on message_id
    with pytest.raises(ValueError, match="Invalid Message ID"):
        funcs.message_unpin(owner_token, 99)

    #Message is already pinned
    with pytest.raises(ValueError, match="Message is already unpinned"):
        funcs.message_unpin(owner_token, message_id)

    #Admin leaves channel
    channel_functions.channel_leave(owner_token, channel)

    #Gets message_id of "This is another valid message"
    message_id = search_function.search(token, \
        "This is another valid message")[0]['messages_id']

    #Admin is not a member of the channel
    with pytest.raises(AccessError, match=\
         "User is not a member of the channel"):
        funcs.message_unpin(owner_token, message_id)

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
