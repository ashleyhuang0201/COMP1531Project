"""
Tests for channel functions
search: Invalid token, successful case (empty search, no such message,
no message in channel, one result from one channel, two results from one
channel, results from multiple channels)
"""
import pytest
import server.search_function as search
from server.Error import AccessError
from server.message_functions import message_send
from server.auth_functions import auth_register
from server.channel_functions import channels_create
from server.helpers import get_user_token_by_u_id
import server.global_var as global_var

# Search given invalid token
def test_search_invalid_token():
    """
    Tests what happens if search is given an invalid token
    """
    with pytest.raises(AccessError, match="Invalid token"):
        # Initialising
        global_var.initialise_all()

        # Creating user
        user = auth_register('user@test.com', 'password', 'search', 'test')
        token = get_user_token_by_u_id(user["u_id"])

        # Creating channel
        channels_create(token, "chat", True)

        search.search("invalid token", "123")

# Search for all
def test_search_all():
    """
    Tests what happens if search is searching using an empty query string
    """
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

    messages = search.search(token, '')

    # Assert the list of messages returned was correct
    assert messages["messages"][0]["message"] == "499"
    assert messages["messages"][0]["u_id"] == user["u_id"]
    assert messages["messages"][1]["message"] == "342"
    assert not messages["messages"][1]["is_pinned"]
    assert messages["messages"][2]["message"] == "321"
    assert messages["messages"][3]["message"] == "121"
    assert messages["messages"][3]["reacts"] == \
         [{"react_id": 1, "u_ids": [], "is_this_user_reacted": False}]

    with pytest.raises(IndexError, match="list index out of range"):
        messages["messages"][4]

    
# Search for message that does not exist and get nothing
def test_search_no_match():
    """
    Tests what happens if search is given a substring with no such string in
    the messages
    """

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
    """
    Test what happens when a search attempt is done on an empty channel
    """
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
    """
    Testing successful case for search with a channel having one message
    and returning one message
    """
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

    messages = search.search(token, '99') 
    assert messages["messages"][0]["message"] == "499"
    assert messages["messages"][0]["u_id"] == user["u_id"]
    with pytest.raises(IndexError, match="list index out of range"):
        messages["messages"][1]

# Search and get 2 messages from the same channel back
def test_search_single_channel():
    """
    Testing successful case for search with a channel having two messages
    and returning two messages
    """
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

    messages = search.search(token, '21')

    assert messages["messages"][0]["message"] == "321"
    assert messages["messages"][0]["u_id"] == user["u_id"]
    assert messages["messages"][1]["message"] == "121"
    with pytest.raises(IndexError, match="list index out of range"):
        messages["messages"][2]

# Search and get 2 messages from different channels back
def test_search_multi_channel():
    """
    Testing successful case of being able to obtain messages from multiple
    channels that the user is apart of
    """
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

    messages = search.search(token, '21')

    assert messages["messages"][0]["message"] == "121"
    assert messages["messages"][0]["u_id"] == user["u_id"]
    assert messages["messages"][1]["message"] == "321"
    with pytest.raises(IndexError, match="list index out of range"):
        messages["messages"][2]