#Functions for testing message_* functions
#Created by: Michael Zhang
#Created on: 29/9/2019

import datetime
import pytest
import message_functions as funcs

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
        funcs.message_send("654321", 1, "This is a valid")

    #The channel based on ID does not exist
    with pytest.raises(ValueError, match = "Invalid Channel ID"):
        funcs.message_send("123456", 2, "This is a valid message")
    
    #A message of length greater than 1000 
    with pytest.raises(ValueError, match = "Message length too long"):
        funcs.message_send("123456", 1, "1" + create_long_string())

    #All errors (Token error is caught first)
    with pytest.raises(ValueError, match = "Invalid Token"):
        funcs.message_send("111111", 2, "1" + create_long_string())


def test_message_remove():
    pass

def test_message_edit():
    pass

def test_message_react():
    pass

def test_message_unreact():
    pass

def test_message_pin():
    pass

def test_message_unpin():
    pass


#Creates a string of 1000 characters for testing purposes
def create_long_string():

    with open('1000characters.txt', 'r') as file:
        longstring = file.read()
    assert len(longstring) == 1000

    return longstring