'''
Test functions for standup_*
'''
import pytest
from server.standup import standup_functions as standup
from server.auth import auth_functions as auth
from server.helper.Error import AccessError
from server.channel import channel_functions as channel_func

def test_standup_start():
    '''
    Test functions for standup_start
    '''
    # A valid token and channel successfully starts a standup - Owner
    owner = auth.auth_register("validcorrect@g.com", "valid_password", \
         "valid_correct_first_name", "valid_correct_last_name")

    channel1 = channel_func.channels_create(owner["token"], "Owner", True)
    channel2 = channel_func.channels_create(owner["token"], "User", True)

    assert standup.standup_start(owner["token"], channel1["channel_id"]) \
        == {"time": get_standup_end()}

    # A valid token and channel successfully starts a standup - User
    user = auth.auth_register("validcorrect@g.com", "valid_password", \
         "valid_correct_first_name", "valid_correct_last_name")

    # User tries to start standup but has not joined the channel
    with pytest.raises(AccessError, match="Cannot Access Channel"):
        standup.standup_start(user["token"], channel2["channel_id"])

    # user starts standup
    channel_func.channel_join(user["token"], channel2["channel_id"])
    assert standup.standup_start(user["token"], channel2["channel_id"]) \
        == {"time": get_standup_end()}

    # Channel id given does not exist
    with pytest.raises(ValueError, match="Channel Does Not Exist"):
        standup.standup_start(user["token"], 21512512521512)

    # Standup works on private channel
    private = channel_func.channels_create(owner["token"], "Owner", False)
    assert standup.standup_start(owner["token"], private["channel_id"]) \
        == {"time": get_standup_end()}

def test_standup_send():
    '''
    Test functions for standup_send
    '''
    # A message is buffered in the standup queue - Owner
    owner = auth.auth_register("validcorrect@g.com", "valid_password", \
         "valid_correct_first_name", "valid_correct_last_name")

    channel = channel_func.channels_create(owner["token"], "Owner", True)

    # Channel is not currently in standup mode
    with pytest.raises(AccessError, match="Not Currently In Standup"):
        standup.standup_send(owner["token"], channel["channel_id"], \
             "correct_and_valid_message")

    standup.standup_start(owner["token"], channel["channel_id"])

    assert standup.standup_send(owner["token"], channel["channel_id"], \
        "correct_and_valid_message") == {}

    user = auth.auth_register("validcorrect1@g.com", "valid_password", \
        "valid_correct_first_name", "valid_correct_last_name")

    # User tries to send message but has not joined channel
    with pytest.raises(AccessError, match="Cannot Access Channel"):
        standup.standup_send(user["token"], channel["channel_id"], \
                  "correct_and_valid_message")

    # A message is buffered in the standup queue - Member
    channel_func.channel_join(user["token"], channel["channel_id"])
    assert standup.standup_send(user["token"], channel["channel_id"], \
        "correct_and_valid_message") == {}

    # Channel given does not exist
    with pytest.raises(ValueError, match="Channel Does Not Exist"):
        standup.standup_send(user["token"], 523523523, \
            "correct_and_valid_message")

    # The message sent was greater than max message length
    with pytest.raises(ValueError, match="Message Too Long"):
        standup.standup_send(user["token"], channel["channel_id"],\
            string_creator(1001))

    # Check still works in private channel
    private = channel_func.channels_create(owner["token"], "Owner", False)
    assert standup.standup_send(owner["token"], private["channel_id"], \
        "correct_and_valid_message") == {}

# Creates a variable length string
def string_creator(length):
    '''
    Helper
    '''
    string = ""
    for _ in range(length):
        string += "a"
    return string

# returns expected end time of standup (15 mins in future)
def get_standup_end():
    '''
    Helper
    '''
    return 900
