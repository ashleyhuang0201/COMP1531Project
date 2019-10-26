"""
Tests for channel functions
search: Invalid token, successful case (empty search, no such message,
no message in channel, 1 result from one channel, two results from one channel,
results from multiple channels)
"""
import pytest
import server.search_function as search
from server.message_functions import message_send
from server.auth_functions import auth_register
from server.channel_functions import channels_create, channel_messages
from server.helpers import get_user_token_by_u_id
import server.global_var as global_var

# Search given invalid token
def test_search_invalid_token():
    with pytest.raises(ValueError, match="Invalid token"):
        # Initialising
        global_var.initialise_all()

        # Creating user
        user = auth_register('user@test.com', 'password', 'search', 'test')
        token = get_user_token_by_u_id(user["u_id"])
        
        # Creating channel
        channel = channels_create(token, "chat", True)
        channel_id = channel["channel_id"]

        search.search("invalid token", "123")

# Search for nothing
def test_search_none():
    # Initialising
    global_var.initialise_all()

    # Creating user
    user = auth_register('user@test.com', 'password', 'search', 'test')
    token = get_user_token_by_u_id(user["u_id"])
    
    # Creating channel
    channel = channels_create(token, "chat", True)
    channel_id = channel["channel_id"]
    
    # Adding messages to channel
    message_send(token, channel_id, "121")
    message_send(token, channel_id, "321")
    message_send(token, channel_id, "342")
    message_send(token, channel_id, "499")
    
    assert search.search(token, '') == {'messages': ['499', '342', '321', '121']}

# Search for message that does not exist and get nothing
def test_search_no_match():
    # Initialising
    global_var.initialise_all()

    # Creating user
    user = auth_register('user@test.com', 'password', 'search', 'test')
    token = get_user_token_by_u_id(user["u_id"])
    
    # Creating channel
    channel = channels_create(token, "chat", True)
    channel_id = channel["channel_id"]
    
    # Adding messages to channel
    message_send(token, channel_id, "121")
    message_send(token, channel_id, "321")
    message_send(token, channel_id, "342")
    message_send(token, channel_id, "499")
    
    assert search.search(token, 'hey') == {'messages': []}

# Search for message with the channel being empty
def test_search_empty_channel():
    # Initialising
    global_var.initialise_all()

    # Creating user
    user = auth_register('user@test.com', 'password', 'search', 'test')
    token = get_user_token_by_u_id(user["u_id"])
    
    # Creating channel
    channel = channels_create(token, "chat", True)
    channel_id = channel["channel_id"]
    
    assert search.search(token, 'hey') == {'messages': []}

# Search and get 1 message back
def test_search_one():
    # Initialising
    global_var.initialise_all()

    # Creating user
    user = auth_register('user@test.com', 'password', 'search', 'test')
    token = get_user_token_by_u_id(user["u_id"])
    
    # Creating channel
    channel = channels_create(token, "chat", True)
    channel_id = channel["channel_id"]
    
    # Adding messages to channel
    message_send(token, channel_id, "121")
    message_send(token, channel_id, "321")
    message_send(token, channel_id, "342")
    message_send(token, channel_id, "499")
    
    assert search.search(token, '99') == {'messages': ['499']}

# Search and get 2 messages from the same channel back
def test_search_single_channel():
    # Initialising
    global_var.initialise_all()

    # Creating user
    user = auth_register('user@test.com', 'password', 'search', 'test')
    token = get_user_token_by_u_id(user["u_id"])
    
    # Creating channel
    channel = channels_create(token, "chat", True)
    channel_id = channel["channel_id"]
    
    # Adding messages to channel
    message_send(token, channel_id, "121")
    message_send(token, channel_id, "321")
    message_send(token, channel_id, "342")
    message_send(token, channel_id, "499")
    
    assert search.search(token, '21') == {'messages': ['321', '121']}

# Search and get 2 messages from different channels back
def test_search_multi_channel():
    # Initialising
    global_var.initialise_all()

    # Creating user
    user = auth_register('user@test.com', 'password', 'search', 'test')
    token = get_user_token_by_u_id(user["u_id"])
    
    # Creating channel 1
    channel1 = channels_create(token, "chat1", True)
    channel1_id = channel1["channel_id"]
    
    # Creating channel 2
    channel2 = channels_create(token, "chat2", True)
    channel2_id = channel2["channel_id"]
    
    # Adding messages to channel
    message_send(token, channel1_id, "121")
    message_send(token, channel2_id, "321")
    
    assert search.search(token, '21') == {'messages': ['121', '321']}
