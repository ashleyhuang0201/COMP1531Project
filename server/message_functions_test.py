#Functions for testing message_* functions
#Created by: Michael Zhang
#Created on: 29/9/2019

import datetime
import message_functions as funcs

# message_sendlater(token, channel_id, message, time_sent)
def test_message_sendlater():

    #A valid send later request is sent
    assert funcs.message_sendlater("123456", 1, "This is a valid message", datetime.datetime(2020,1,1)) == "Successful"
    #A invalid token is sent to the function (A invalid user is trying to use the function)
    assert funcs.message_sendlater("111111", 1, "This is a valid message", datetime.datetime(2020,1,1)) == "Token Error"
    #The channel based on ID does not exist
    assert funcs.message_sendlater("123456", 2, "This is a valid message", datetime.datetime(2020,1,1)) == "Channel Error"
    #A message of length 1000 characters is valid
    assert funcs.message_sendlater("123456", 1, create_long_string(), datetime.datetime(2020,1,1)) == "Successful"
    #A message of length greater than 1000 
    assert funcs.message_sendlater("123456", 1, "1" + create_long_string(), datetime.datetime(2020,1,1)) == "Message Error"
    #Time sent is a time in the past 
    assert funcs.message_sendlater("123456", 1, "This is a valid message", datetime.datetime(2019,1,1)) == "Time Error"
    #All errors (Token error is caught first)
    assert funcs.message_sendlater("111111", 2, "1" + create_long_string(), datetime.datetime(2019,1,1)) == "Token Error"


def test_message_send():
    pass

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