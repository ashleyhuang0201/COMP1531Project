# Tests for the search messages function
# Created by: Coen Townson
# Created on: 2/10/2019

import pytest
import search_function as search
import message_functions as message
import auth_functions as auth
import channel_functions as channel

##### Initialize some messages to be searched #####
# Create test user
user = auth.auth_register('searchtest@test.com', 'password', 'search', 'test')
# Create two test channels to ensure search covers both
channel1 = channel.channels_create(user['token'], "Test1", True)
channel2 = channel.channels_create(user['token'], "Test2", True)
# Send some messages
message.message_send(user['token'], channel1, '93336255 Singlechannel match 1')
message.message_send(user['token'], channel1, '93336255 Singlechannel match 2')
message.message_send(user['token'], channel1, '93336256 Only this')
message.message_send(user['token'], channel1, '93336257 Multichannel search 1')
message.message_send(user['token'], channel2, '93336257 Multichannel search 2')

# Get a list of the messages just created
messages1 = channel.channel_messages(user['token'], channel1, 0)
messages2 = channel.channel_messages(user['token'], channel2, 0)

##### Tests #####

# Search for nothing and get nothing
def test_search_none():
    assert search.search(user['token'], '') == []

# Search for message that shouldn't exist and get nothing
def test_search_empty():
    assert search.search(user['token'], '63331448511 this is a bad search and should not be filled') == []

# Search and get 1 message back
def test_search_one():
    assert search.search(user['token'], '93336256 Only this') == messages1[1]

# Search and get 2 messages from the same channel back
def test_search_single_channel():
    assert search.search(user['token'], '93336255 Singlechannel match ') == [messages1[2], messages1[3]]

# Search and get 2 messages from different channels back
def test_search_multi_channel():
    assert search.search(user['token'], '93336257 Multichannel search ') == [messages2[0], messages1[0]]
