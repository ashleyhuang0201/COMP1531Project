#Functions for testing message_* functions
#Created by: Michael Zhang
#Created on: 29/9/2019

import datetime
import pytest
import message_functions as funcs
from Error import AccessError

# message_sendlater(token, channel_id, message, time_sent)
def test_message_sendlater():

    #A valid send later request is sent
    funcs.message_sendlater("123456", 1, "This is a valid message", datetime.datetime(2020,1,1))

    #A message of length 1000 characters is valid
    funcs.message_sendlater("123456", 1, create_long_string(), datetime.datetime(2020,1,1))

    #An exception is thrown if a invalid token is given
    with pytest.raises(ValueError, match = "Invalid Token"):
        funcs.message_sendlater("111111", 1, "This is a valid message", datetime.datetime(2020,1,1))

    #The channel based on ID does not exist
    with pytest.raises(ValueError, match = "Invalid Channel ID"):
        funcs.message_sendlater("123456", 2, "This is a valid message", datetime.datetime(2020,1,1))
        
    #A message of length greater than 1000 
    with pytest.raises(ValueError, match = "Message length too long"):
        funcs.message_sendlater("123456", 1, "1" + create_long_string(), datetime.datetime(2020,1,1))

    #Time sent is a time in the past 
    with pytest.raises(ValueError, match = "Time sent was in the past"):
        funcs.message_sendlater("123456", 1, "This is a valid message", datetime.datetime(2019,1,1))

    #All errors (Token error is caught first)
    with pytest.raises(ValueError, match = "Invalid Token"):
        funcs.message_sendlater("111111", 2, "1" + create_long_string(), datetime.datetime(2019,1,1))
        

# message_send(token, channel_id, message)
def test_message_send():
    
    #A valid send request is sent
    funcs.message_send("123456", 1, "This is a valid message")

    #A message of length 1000 characters is valid
    funcs.message_send("123456", 1, create_long_string())

    #A invalid token is sent to the function (A invalid user is trying to use the function)
    with pytest.raises(ValueError, match = "Invalid Token"):
        funcs.message_send("111111", 1, "This is a valid")

    #The channel based on ID does not exist
    with pytest.raises(ValueError, match = "Invalid Channel ID"):
        funcs.message_send("123456", 2, "This is a valid message")
    
    #A message of length greater than 1000 
    with pytest.raises(ValueError, match = "Message length too long"):
        funcs.message_send("123456", 1, "1" + create_long_string())

    #All errors (Token error is caught first)
    with pytest.raises(ValueError, match = "Invalid Token"):
        funcs.message_send("111111", 2, "1" + create_long_string())


# message_remove(token, message_id):
def test_message_remove():
    
    #A owner removes a valid message
    funcs.message_remove("owner", 1)

    #A user removes his own message
    funcs.message_remove("123456", 1)

    #A owner tries to remove a invalid message based on message_id
    with pytest.raises(ValueError, match = "Invalid Message ID"):
        funcs.message_remove("owner", 99)

    #A user tries to remove a invalid message based on message_id 
    with pytest.raises(ValueError, match = "Invalid Message ID"):
        funcs.message_remove("123456", 99)

    #A user tries to remove a message not his
    with pytest.raises(AccessError, match = "User does not have permission"):
        funcs.message_remove("223456", 1)


# message_edit(token, message_id, message):
def test_message_edit():
    
    #A owner edits a valid message
    funcs.message_edit("owner", 1, "This is a valid message")

    #A user edits his own message
    funcs.message_edit("123456", 1, "This is a valid message")

    #A owner tries to edit a invalid message based on message_id
    with pytest.raises(ValueError, match = "Invalid Message ID"):
        funcs.message_edit("owner", 99, "This is a valid message")

    #A user tries to edit a invalid message based on message_id 
    with pytest.raises(ValueError, match = "Invalid Message ID"):
        funcs.message_edit("123456", 99, "This is a valid message")

    #A user tries to edit a message not his
    with pytest.raises(AccessError, match = "User does not have permission"):
        funcs.message_edit("223456", 1, "This is a valid message")

    #The edited message was too long
    with pytest.raises(ValueError, match = "Message length too long"):
        funcs.message_edit("owner", 1, "1" + create_long_string())


# message_react(token, message_id, react_id):
def test_message_react():
    
    #A user successfully reacts
    funcs.message_react("123456", 1, 1)

    #A user tries to react to a invalid message based on message_id
    with pytest.raises(ValueError, match = "Invalid Message ID"):
        funcs.message_react("owner", 99, 1)

    #A user tries to react to a message already reacted to
    with pytest.raises(ValueError, match = "Message contains a active react"):
        funcs.message_react("123456", 2, 1)

    #A user uses a invalid react id
    with pytest.raises(ValueError, match = "Invalid React ID"):
        funcs.message_react("123456", 1, 99)


# message_unreact(token, message_id, react_id):
def test_message_unreact():
    
    #A user successfully unreacts
    funcs.message_unreact("123456", 2, 1)

    #A user tries to unreact to a invalid message based on message_id
    with pytest.raises(ValueError, match = "Invalid Message ID"):
        funcs.message_unreact("owner", 99, 1)

    #A user tries to unreact to a message that is not reacted to
    with pytest.raises(ValueError, match = "Message does not contains a active react"):
        funcs.message_unreact("123456", 1, 1)

    #A user uses a invalid react id
    with pytest.raises(ValueError, match = "Invalid React ID"):
        funcs.message_unreact("123456", 1, 99)


# message_pin(token, message_id):
def test_message_pin():
    
    #A user successfully pins a message
    funcs.message_pin("admin_member", 1)

    #Message is invalid based on message_id
    with pytest.raises(ValueError, match = "Invalid Message ID"):
        funcs.message_pin("admin_member", 99)

    #A user is not an admin
    with pytest.raises(ValueError, match = "Not an admin"):
        funcs.message_pin("123456", 1)

    #Message is already pinned
    with pytest.raises(ValueError, match = "Message is already pinned"):
        funcs.message_pin("admin_member", 2)

    #Admin is not a member of the channel
    with pytest.raises(AccessError, match = "User is not a member of the channel"):
        funcs.message_pin("admin_nonmember", 1)


def test_message_unpin():
    
    #A user successfully unpins a message
    funcs.message_unpin("admin_member", 2)

    #Message is invalid based on message_id
    with pytest.raises(ValueError, match = "Invalid Message ID"):
        funcs.message_unpin("admin_member", 99)

    #A user is not an admin
    with pytest.raises(ValueError, match = "Not an admin"):
        funcs.message_unpin("123456", 2)

    #Message is already pinned
    with pytest.raises(ValueError, match = "Message is already unpinned"):
        funcs.message_unpin("admin_member", 1)

    #Admin is not a member of the channel
    with pytest.raises(AccessError, match = "User is not a member of the channel"):
        funcs.message_unpin("admin_nonmember", 2)


#Creates a string of 1000 characters for testing purposes
def create_long_string():

    with open('1000characters.txt', 'r') as file:
        longstring = file.read()
    assert len(longstring) == 1000

    return longstring