'''
Tests for the search messages function
Created by: Coen Townson
Created on: 2/10/2019
'''

from server.search import search_function as search
from server.message.message_functions import message_send
from server.auth.auth_functions import auth_register
from server.channel.channel_functions import channels_create, channel_messages

##### Initialize some messages to be searched #####
# Create test user
USER = auth_register('searchtest@test.com', 'password', 'search', 'test')
# Create two test channels to ensure search covers both
CHANNEL1 = channels_create(USER['token'], "Test1", True)
CHANNEL2 = channels_create(USER['token'], "Test2", True)
# Send some messages
message_send(USER['token'], CHANNEL1, '93336255 Singlechannel match 1')
message_send(USER['token'], CHANNEL1, '93336255 Singlechannel match 2')
message_send(USER['token'], CHANNEL1, '93336256 Only this')
message_send(USER['token'], CHANNEL1, '93336257 Multichannel search 1')
message_send(USER['token'], CHANNEL2, '93336257 Multichannel search 2')

# Get a list of the messages just created
MESSAGES1 = channel_messages(USER['token'], CHANNEL1, 0)
MESSAGES2 = channel_messages(USER['token'], CHANNEL2, 0)

##### Tests #####

# Search for nothing and get nothing
def test_search_none():
    '''
    Tests search of nothing
    '''
    assert search.search(USER['token'], '') == {'messages': []}

# Search for message that shouldn't exist and get nothing
def test_search_empty():
    '''
    Tests search with no results
    '''
    assert search.search(USER['token'], 'no message here like this') == \
        {'messages': []}

# Search and get 1 message back
def test_search_one():
    '''
    Tests search of one result
    '''
    assert search.search(USER['token'], '93336256 Only this') == \
        {'messages': MESSAGES1[1]}

# Search and get 2 messages from the same channel back
def test_search_single_channel():
    '''
    Tests search of multiple results in one channel
    '''
    assert search.search(USER['token'], '93336255 Singlechannel match ') == \
        {'messages': [MESSAGES1[2], MESSAGES1[3]]}

# Search and get 2 messages from different channels back
def test_search_multi_channel():
    '''
    Tests search of multiple results across multiple channels
    '''
    assert search.search(USER['token'], '93336257 Multichannel search ') == \
        {'messages': [MESSAGES2[0], MESSAGES1[0]]}
