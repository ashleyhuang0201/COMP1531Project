'''
Tests for channel functions
search: Invalid token, successful case (empty search, no such message, no
message in channel, one result from one channel, two results from one channel,
results from multiple channels)
'''
import pytest
import server.global_var as global_var
import server.search_function as search
from server.auth_functions import auth_register
from server.channel_functions import channels_create
from server.constants import HEART_REACT, LIKE_REACT
from server.Error import AccessError
from server.helpers import get_user_token_by_u_id
from server.message_functions import message_send

# Search given invalid token
def test_search_invalid_token():
    '''
    Testing search with an invalid token
    '''
    with pytest.raises(AccessError, match="Invalid token"):
        # Initialising
        global_var.initialise_all()

        # Creating user
        user = auth_register('user@test.com', 'password', 'search', 'test')
        token = get_user_token_by_u_id(user["u_id"])

        # Creating channel
        channels_create(token, "chat", True)

        # Searching using an invalid token
        search.search("invalid token", "123")

# Search for all
def test_search_all():
    '''
    Testing search with a search for all messages request
    '''
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

    # Searching for all messages
    messages = search.search(token, '')

    # Checking if all messages are retrieved
    assert messages["messages"][0]["message"] == "499"
    assert messages["messages"][0]["u_id"] == user["u_id"]
    assert messages["messages"][1]["message"] == "342"
    assert not messages["messages"][1]["is_pinned"]
    assert messages["messages"][2]["message"] == "321"
    assert messages["messages"][3]["message"] == "121"
    assert messages["messages"][3]["reacts"] == [
        {
            "react_id": LIKE_REACT,
            "u_ids": [],
            "is_this_user_reacted": False
        },
        {
            "react_id": HEART_REACT,
            "u_ids": [],
            "is_this_user_reacted": False
        }
    ]

    # Ensuring that no messages after all messages retrieved
    with pytest.raises(IndexError, match="list index out of range"):
        message = messages["messages"][4]

# Search for message that does not exist
def test_search_no_match():
    '''
    Testing search with a search for no such message
    '''

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
    '''
    Test search with a search on an empty channel
    '''
    # Initialising
    global_var.initialise_all()

    # Creating user
    user = auth_register('user@test.com', 'password', 'search', 'test')
    token = get_user_token_by_u_id(user["u_id"])

    # Creating channel
    channels_create(token, "chat", True)

    assert search.search(token, 'hey') == {'messages': []}

# Search and get one message back
def test_search_one():
    '''
    Testing successful case for a search for one message
    '''

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

    # Searching message
    messages = search.search(token, '99')

    # Checking if message obtained
    assert messages["messages"][0]["message"] == "499"
    assert messages["messages"][0]["u_id"] == user["u_id"]

    # Ensuring that no other messages are obtained
    with pytest.raises(IndexError, match="list index out of range"):
        message = messages["messages"][1]

# Search and get 2 messages from the same channel back
def test_search_single_channel():
    '''
    Testing successful case for search with a channel having two messages
    and returning two messages
    '''

    # Initialising
    global_var.initialise_all()

    # Creating user
    user = auth_register('user@test.com', 'password', 'search', 'test')
    token = get_user_token_by_u_id(user["u_id"])

    user2 = auth_register('user2@test.com', 'password', 'search', 'test')
    token2 = get_user_token_by_u_id(user2["u_id"])

    # Creating channel
    channel = channels_create(token, "chat", True)
    channel_id = channel["channel_id"]

    # Create channel from the second user which the searching user is not a
    # member of
    channels_create(token2, "chat", True)

    # Adding messages to channel
    message_send(token, channel_id, "121")
    message_send(token, channel_id, "321")
    message_send(token, channel_id, "342")
    message_send(token, channel_id, "499")

    # Search
    messages = search.search(token, '21')

    # Checking if messages are obtained
    assert messages["messages"][0]["message"] == "321"
    assert messages["messages"][0]["u_id"] == user["u_id"]
    assert messages["messages"][1]["message"] == "121"

    # Ensuring that no other messages are obtained
    with pytest.raises(IndexError, match="list index out of range"):
        message = messages["messages"][2]

# Search and get 2 messages from different channels back
def test_search_multi_channel():
    '''
    Testing successful case of being able to obtain messages from multiple
    channels that the user is apart of
    '''
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

    # Search
    messages = search.search(token, '21')

    # Checking if messages obtained
    assert messages["messages"][0]["message"] == "121"
    assert messages["messages"][0]["u_id"] == user["u_id"]
    assert messages["messages"][1]["message"] == "321"

    # Ensuring that no other messages are obtained
    with pytest.raises(IndexError, match="list index out of range"):
        message = messages["messages"][2]
