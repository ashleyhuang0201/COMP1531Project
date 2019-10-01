#Dummy implementations of functions message_*
#Created by: Michael Zhang
#Created on: 29/9/2019

#Date module for representing time
import datetime
import pytest
from Error import AccessError

"""
Sends a message from authorised_user to the channel specified by channel_id automatically at a specified
time in the future

Data types:
token: string
channel_id: integer
message: string
time_sent: datetime

ValueErrors:
- Channel based on ID does not exist
- Message is more than 1000 Characters
- Time sent is a time in the past
"""
def message_sendlater(token, channel_id, message, time_sent):
    
    #A exception is thrown if any values are invalid
    if valid_token(token) == False:
        raise ValueError("Invalid Token")
    elif valid_channel(channel_id) == False:
        raise ValueError("Invalid Channel ID")
    elif len(message) > 1000:
        raise ValueError("Message length too long")
    elif(time_sent < datetime.datetime.now()):
        raise ValueError("Time sent was in the past")

    #The message is valid and will be sent to the channel at the specific time
    
"""
Send a message from authorised_user to the channel specified by channel_id

Data types:
token: string
channel_id: integer
message: string

ValueErrors:
- Message is more than 1000 Characters
"""
def message_send(token, channel_id, message):
    
    #A exception is thrown if any values are invalid
    if valid_token(token) == False:
        raise ValueError("Invalid Token")
    elif valid_channel(channel_id) == False:
        raise ValueError("Invalid Channel ID")
    elif len(message) > 1000:
        raise ValueError("Message length too long")

    #The message is valid and is sent to the channel

"""
Given a message ID, the message is removed

Data types:
token: string
message_id: integer

ValueErrors:
- Message no longer exists (Based on ID)
AccessErrors:
- User does not have permission to remove that row
"""
def message_remove(token, message_id):

    if valid_token(token) == False:
        raise ValueError("Invalid Token")
    elif valid_message_id(message_id) == False:    
        raise ValueError("Invalid Message ID")
    elif valid_permission(token, message_id) == False:
        raise AccessError("User does not have permission")

    #The message is removed from the channel

"""
Given a message, update it's text with new text

Data types:
token: string
message_id: integer
message: string

ValueErrors:
- message_id is not a valid message when it is not:
    1) a message sent by the authorised user
    2) If the authorised user is an admin, is any message within a channel that the authorised user has joined
"""
def message_edit(token, message_id, message):

    if valid_token(token) == False:
        raise ValueError("Invalid Token")
    elif valid_message_id(message_id) == False:    
        raise ValueError("Invalid Message ID")
    elif valid_permission(token, message_id) == False:
        raise AccessError("User does not have permission")
    elif len(message) > 1000:
        raise ValueError("Message length too long")
    
    #The message is edited


"""
Given a message within a channel the authorised user is part of, add a "react" to that particular message

Data types:
token: string
message_id: integer
react_id: integer

ValueErrors:
- message_id is not a valid message within a channel that the authorised user has joined
- react_id is not a valid react ID
- Message with ID message_id already contains a active react with ID react_id
"""
def message_react(token, message_id, react_id):

    #React status of messages
    messages_reacts = [0,0,1]
    
    if valid_message_id(message_id) == False:
        raise ValueError("Invalid Message ID")
    elif valid_react_id(react_id) == False:
        raise ValueError("Invalid React ID")
    #The message with message_id already contains an active react
    elif messages_reacts[message_id] == 1:
        raise ValueError("Message contains a active react")

    #React status of message is set
    messages_reacts[message_id] = 1
    
"""
Given a message within a channel the authorised user is part of, remove a "react" to that particular message

Data types:
token: string
message_id: integer
react_id: integer

ValueErrors:
- message_id is not a valid message within a channel that the authorised user has joined
- react_id is not a valid react ID
- Message with ID message_id does not contain an active react with ID react_id
"""
def message_unreact(token, message_id, react_id):
    
    #React status of messages
    messages_reacts = [0,0,1]

    if valid_message_id(message_id) == False:
        raise ValueError("Invalid Message ID")
    elif valid_react_id(react_id) == False:
        raise ValueError("Invalid React ID")
    #The message with message_id already contains an active react
    elif messages_reacts[message_id] == 0:
        raise ValueError("Message does not contains a active react")
    
    messages_reacts[message_id] = 0

"""
Given a message within a channel, mark it as "pinned" to be given special display treatment by the frontend

Data types:
token: string
message_id: integer

ValueErrors:
- message_id is not a valid message
- The authorised user is not an admin
- Message with ID message_id is already pinned
AccessErrors:
- The authorised user is not a member of the channel that the message is within
"""
def message_pin(token, message_id):

    #Message pin status
    messages_pinned = [0,0,1]

    if valid_message_id(message_id) == False:
        raise ValueError("Invalid Message ID")
    elif token != "admin_member" and token != "admin_nonmember":
        raise ValueError("Not an admin")
    elif messages_pinned[message_id] == 1:
        raise ValueError("Message is already pinned")
    elif token == "admin_nonmember":
        raise AccessError("User is not a member of the channel")

    messages_pinned[message_id] == 1

"""
Given a message within a channel, remove it's mark as unpinned

Data types:
token: string
message_id: integer

ValueErrors:
- message_id is not a valid message
- The authorised user is not a admin
- Message with ID message_id is already unpinned
"""
def message_unpin(token, message_id):

    #Message pin status
    messages_pinned = [0,0,1]

    if valid_message_id(message_id) == False:
        raise ValueError("Invalid Message ID")
    elif token != "admin_member" and token != "admin_nonmember":
        raise ValueError("Not an admin")
    elif messages_pinned[message_id] == 0:
        raise ValueError("Message is already unpinned")
    elif token == "admin_nonmember":
        raise AccessError("User is not a member of the channel")

    messages_pinned[message_id] == 0

# Checks the validity of a token
def valid_token(token):
    if token == "123456" or token == "223456" or token == "owner":
        # Active token
        return True
    else:
        # Inactive token
        return False

# Checks that the channel_id belongs to a existing channel
# 1 = valid channel_id, anything else is a invalid channel_id
def valid_channel(channel_id):
    if channel_id == 1:
        return True
    else:
        return False

#Checks that the message_id belongs to a existing channel
# 1 = valid message_id, anything else is a invalid message_id
def valid_message_id(message_id):
    if message_id == 0 or message_id == 1 or message_id == 2:
        return True
    else:
        return False

def valid_permission(token, message_id):

    #User is a owner
    if token == "owner":
        return True
    #The message was a message sent by the user
    elif message_id == int(token[0]):
        return True

    return False

def valid_react_id(react_id):

    if react_id == 1:
        return True

    return False