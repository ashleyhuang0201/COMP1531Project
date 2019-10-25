"""
Tests for channel functions
search: Invalid token, successful case (empty search, no such message,
no message in channel, 1 result from one channel, two results from one channel,
results from multiple channels)
"""
import pytest
from server.search import search_function as search
from server.message.message_functions import message_send
from server.auth.auth_functions import auth_register
from server.channel.channel_functions import channels_create, channel_messages

# Search given invalid token
def test_search_invalid_token:
    with pytest.raises(ValueError, match="Invalid token"):
        # Creating user
        user = auth_register('user@test.com', 'password', 'search', 'test')
        token = get_user_by_u_id(user.u_id)
        
        # Creating channel
        channel = channels_create(token, "chat", True)
        channel_id = channel["channel_id"]

        search.search("invalid token", "123")

# Search for nothing
def test_search_none():
    # Creating user
    user = auth_register('user@test.com', 'password', 'search', 'test')
    token = get_user_by_u_id(user.u_id)
    
    # Creating channel
    channel = channels_create(token, "chat", True)
    channel_id = channel["channel_id"]
    
    # Adding messages to channel
    def message_send(token, channel_id, "121"):
    def message_send(token, channel_id, "321"):
    def message_send(token, channel_id, "342"):
    def message_send(token, channel_id, "499"):
    
    assert search.search(token, '') == {'messages': []}

# Search for message that does not exist and get nothing
def test_search_no_match():
    # Creating user
    user = auth_register('user@test.com', 'password', 'search', 'test')
    token = get_user_by_u_id(user.u_id)
    
    # Creating channel
    channel = channels_create(token, "chat", True)
    channel_id = channel["channel_id"]
    
    # Adding messages to channel
    def message_send(token, channel_id, "121"):
    def message_send(token, channel_id, "321"):
    def message_send(token, channel_id, "342"):
    def message_send(token, channel_id, "499"):
    
    assert search.search(token, 'hey') == {'messages': []}

# Search for message with the channel being empty
def test_search_empty_channel():
    # Creating user
    user = auth_register('user@test.com', 'password', 'search', 'test')
    token = get_user_by_u_id(user.u_id)
    
    # Creating channel
    channel = channels_create(token, "chat", True)
    channel_id = channel["channel_id"]
    
    assert search.search(token, 'hey') == {'messages': []}

# Search and get 1 message back
def test_search_one():
    # Creating user
    user = auth_register('user@test.com', 'password', 'search', 'test')
    token = get_user_by_u_id(user.u_id)
    
    # Creating channel
    channel = channels_create(token, "chat", True)
    channel_id = channel["channel_id"]
    
    # Adding messages to channel
    def message_send(token, channel_id, "121"):
    def message_send(token, channel_id, "321"):
    def message_send(token, channel_id, "342"):
    def message_send(token, channel_id, "499"):
    
    assert search.search(token, '99') == {'messages': ['499']}

# Search and get 2 messages from the same channel back
def test_search_single_channel():
    # Creating user
    user = auth_register('user@test.com', 'password', 'search', 'test')
    token = get_user_by_u_id(user.u_id)
    
    # Creating channel
    channel = channels_create(token, "chat", True)
    channel_id = channel["channel_id"]
    
    # Adding messages to channel
    def message_send(token, channel_id, "121"):
    def message_send(token, channel_id, "321"):
    def message_send(token, channel_id, "342"):
    def message_send(token, channel_id, "499"):
    
    assert search.search(token, '21') == {'messages': ['121', '321']}

# Search and get 2 messages from different channels back
def test_search_multi_channel():
    # Creating user
    user = auth_register('user@test.com', 'password', 'search', 'test')
    token = get_user_by_u_id(user.u_id)
    
    # Creating channel 1
    channel1 = channels_create(token, "chat1", True)
    channel1_id = channel1["channel_id"]
    
    # Creating channel 2
    channel2 = channels_create(token, "chat2", True)
    channel2_id = channel2["channel_id"]
    
    # Adding messages to channel
    def message_send(token, channel1_id, "121"):
    def message_send(token, channel2_id, "321"):
    
    assert search.search(token, '21') == {'messages': ['121', '321']}
