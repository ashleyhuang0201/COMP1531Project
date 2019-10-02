#Functions for testing message_* functions
#Created by: Michael Zhang
#Created on: 29/9/2019

import datetime
import pytest
import message_functions as funcs
import auth_functions
from Error import AccessError

# message_sendlater(token, channel_id, message, time_sent)  
def test_message_sendlater():

    #Initialisation
    user = auth_functions.auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name")
    token = user["token"]
    #Use function from channel_functions.py once Ashley implements them
    #channel = channels_create(token,"Name", True)
    channel = 1

    #A valid send later request is sent
    assert funcs.message_sendlater(token, channel, "This is a valid message", datetime.datetime(2020,1,1)) == {}

    #A message of length 1000 characters is valid
    assert funcs.message_sendlater(token, channel, create_long_string(), datetime.datetime(2020,1,1)) == {}

    #A message of length greater than 1000 is valid
    with pytest.raises(ValueError, match = "Message length too long"):
        funcs.message_sendlater(token, channel, "1" + create_long_string(), datetime.datetime(2020,1,1))

    #An exception is thrown if a invalid token is given
    with pytest.raises(ValueError, match = "Invalid Token"):
        funcs.message_sendlater("111111", channel, "This is a valid message", datetime.datetime(2020,1,1))

    #The channel based on ID does not exist
    with pytest.raises(ValueError, match = "Invalid Channel ID"):
        funcs.message_sendlater(token, 99, "This is a valid message", datetime.datetime(2020,1,1))
          
    #Time sent is a time in the past 
    with pytest.raises(ValueError, match = "Time sent was in the past"):
        funcs.message_sendlater(token, channel, "This is a valid message", datetime.datetime(2019,1,1))

    #All errors (Token error is caught first)
    with pytest.raises(ValueError, match = "Invalid Token"):
        funcs.message_sendlater("111111", 99, "1" + create_long_string(), datetime.datetime(2019,1,1))
        

# message_send(token, channel_id, message)
def test_message_send():

    #Initialisation
    user = auth_functions.auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name")
    token = user["token"]
    #Use function from channel_functions.py once Ashley implements them
    #channel = channels_create(token,"Name", True)
    channel = 1
    
    #A valid send request is sent
    assert funcs.message_send(token, channel, "This is a valid message") == {}

    #A message of length 1000 characters is valid
    assert funcs.message_send(token, channel, create_long_string()) == {}

    #A invalid token is sent to the function (A invalid user is trying to use the function)
    with pytest.raises(ValueError, match = "Invalid Token"):
        funcs.message_send("111111", channel, "This is a valid message")

    #The channel based on ID does not exist
    with pytest.raises(ValueError, match = "Invalid Channel ID"):
        funcs.message_send(token, 99, "This is a valid message")
    
    #A message of length greater than 1000 
    with pytest.raises(ValueError, match = "Message length too long"):
        funcs.message_send(token, channel, "1" + create_long_string())

    #All errors (Token error is caught first)
    with pytest.raises(ValueError, match = "Invalid Token"):
        funcs.message_send("111111", 99, "1" + create_long_string())


# message_remove(token, message_id)
def test_message_remove():

    #Initialisation
    user = auth_functions.auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name")
    token = user["token"]
    #Use function from channel_functions.py once Ashley implements them
    #channel = channels_create(token,"Name", True)
    channel = 1

    funcs.message_send(token, channel, "This is a valid message")
    funcs.message_send(token, channel, "This is another valid message")

    #A owner removes a valid message
    assert funcs.message_remove("owner", 1) == {}

    #A user removes his own message
    assert funcs.message_remove(token, 1) == {}

    #A owner tries to remove a invalid message based on message_id
    with pytest.raises(ValueError, match = "Invalid Message ID"):
        funcs.message_remove("owner", 99)

    #A user tries to remove a invalid message based on message_id 
    with pytest.raises(ValueError, match = "Invalid Message ID"):
        funcs.message_remove(token, 99)

    #A user tries to remove a message not his
    with pytest.raises(AccessError, match = "User does not have permission"):
        funcs.message_remove("223456", 1)


# message_edit(token, message_id, message)
def test_message_edit():

    #Initialisation
    user = auth_functions.auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name")
    token = user["token"]

    #A owner edits a valid message
    assert funcs.message_edit("owner", 1, "This is a valid message") == {}

    #A user edits his own message
    assert funcs.message_edit(token, 1, "This is a valid message") == {}

    #A owner tries to edit a invalid message based on message_id
    with pytest.raises(ValueError, match = "Invalid Message ID"):
        funcs.message_edit("owner", 99, "This is a valid message")

    #A user tries to edit a invalid message based on message_id 
    with pytest.raises(ValueError, match = "Invalid Message ID"):
        funcs.message_edit(token, 99, "This is a valid message")

    #A user tries to edit a message not his
    with pytest.raises(AccessError, match = "User does not have permission"):
        funcs.message_edit("223456", 1, "This is a valid message")

    #The edited message was too long
    with pytest.raises(ValueError, match = "Message length too long"):
        funcs.message_edit("owner", 1, "1" + create_long_string())


# message_react(token, message_id, react_id)
def test_message_react():

    #Initialisation
    user = auth_functions.auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name")
    token = user["token"]
    
    #A user successfully reacts
    assert funcs.message_react(token, 1, 1) == {}

    #A user tries to react to a invalid message based on message_id
    with pytest.raises(ValueError, match = "Invalid Message ID"):
        funcs.message_react("owner", 99, 1)

    #A user tries to react to a message already reacted to
    with pytest.raises(ValueError, match = "Message contains a active react"):
        funcs.message_react(token, 3, 1)

    #A user uses a invalid react id
    with pytest.raises(ValueError, match = "Invalid React ID"):
        funcs.message_react(token, 1, 99)


# message_unreact(token, message_id, react_id)
def test_message_unreact():
    
    #Initialisation
    user = auth_functions.auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name")
    token = user["token"]

    #A user successfully unreacts
    assert funcs.message_unreact(token, 3, 1) == {}

    #A user tries to unreact to a invalid message based on message_id
    with pytest.raises(ValueError, match = "Invalid Message ID"):
        funcs.message_unreact("owner", 99, 1)

    #A user tries to unreact to a message that is not reacted to
    with pytest.raises(ValueError, match = "Message does not contains a active react"):
        funcs.message_unreact(token, 1, 1)

    #A user uses a invalid react id
    with pytest.raises(ValueError, match = "Invalid React ID"):
        funcs.message_unreact(token, 1, 99)


# message_pin(token, message_id)
def test_message_pin():
    
    #Initialisation
    user = auth_functions.auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name")
    token = user["token"]

    #A user successfully pins a message
    assert funcs.message_pin("admin_member", 1) == {}

    #Message is invalid based on message_id
    with pytest.raises(ValueError, match = "Invalid Message ID"):
        funcs.message_pin("admin_member", 99)

    #A user is not an admin
    with pytest.raises(ValueError, match = "Not an admin"):
        funcs.message_pin(token, 1)

    #Message is already pinned
    with pytest.raises(ValueError, match = "Message is already pinned"):
        funcs.message_pin("admin_member", 3)

    #Admin is not a member of the channel
    with pytest.raises(AccessError, match = "User is not a member of the channel"):
        funcs.message_pin("admin_nonmember", 1)


# message_unpin(token, message_id)
def test_message_unpin():

    #Initialisation
    user = auth_functions.auth_register("valid_correct_email", "valid_correct_password", "valid_correct_first_name", "valid_correct_last_name")
    token = user["token"]
    
    #A user successfully unpins a message
    assert funcs.message_unpin("admin_member", 3) == {}

    #Message is invalid based on message_id
    with pytest.raises(ValueError, match = "Invalid Message ID"):
        funcs.message_unpin("admin_member", 99)

    #A user is not an admin
    with pytest.raises(ValueError, match = "Not an admin"):
        funcs.message_unpin(token, 3)

    #Message is already pinned
    with pytest.raises(ValueError, match = "Message is already unpinned"):
        funcs.message_unpin("admin_member", 1)

    #Admin is not a member of the channel
    with pytest.raises(AccessError, match = "User is not a member of the channel"):
        funcs.message_unpin("admin_nonmember", 3)

#Helper Functions

#Creates a string of 1000 characters for testing purposes
def create_long_string():
    longstring = ""
    for i in range(1000):
        longstring += "a"
    assert len(longstring) == 1000

    return longstring