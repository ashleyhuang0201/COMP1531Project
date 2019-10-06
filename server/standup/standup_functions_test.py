from server.standup import standup_functions as standup
from server.auth import auth_functions as auth
import pytest
from server.helper.Error import AccessError
from server.channel import channel_functions as channel

def test_standup_start():
    # A valid token and channel successfully starts a standup - Owner
    user = auth.auth_register("validcorrect@g.com", "valid_password", \
         "valid_correct_first_name", "valid_correct_last_name")
    channel = channel.channels_create(user["token"], "Group Name", True)
    assert standup.standup_start(user["token"], channel["channel_id"]) \
        == {"time": 900}
    # A valid token and channel successfully starts a standup - User
    owner = auth.auth_register("validcorrect@g.com", "valid_password", \
         "valid_correct_first_name", "valid_correct_last_name")
    channel = channel.channels_create(owner["token"], "Group Name", True)
    user = auth.auth_register("validcorrect1@g.com", "valid_password", \
         "valid_correct_first_name", "valid_correct_last_name")
    assert standup.standup_start(user["token"], channel["channel_id"]) \
        == {"time": 900}
    # Channel id given does not exist
    with pytest.raises(ValueError, match = "Channel Does Not Exist"):
        user = auth.auth_register("validcorrect@g.com", "valid_password", \
            "valid_correct_first_name", "valid_correct_last_name")
        standup.standup_start(user["token"], 21512512521512)
    # User has not joined the channel
    with pytest.raises(AccessError, match = "Cannot Access Channel"):
        owner = auth.auth_register("validcorrect@g.com", "valid_password", \
            "valid_correct_first_name", "valid_correct_last_name")
        channel = channel.channels_create(owner["token"], "Group Name", True)
        user = auth.auth_register("validcorrect1@g.com", "valid_password", \
            "valid_correct_first_name", "valid_correct_last_name")
        time = standup.standup_start(user["token"], channel["channel_id"])

def test_standup_send():
    # A message is buffered in the standup queue - Owner
    user = auth.auth_register("validcorrect@g.com", "valid_password", \
         "valid_correct_first_name", "valid_correct_last_name")
    channel = channel.channels_create(user["token"], "Group Name", True)
    time = standup.standup_start(user["token"], channel["channel_id"])
    assert standup.standup_send(user["token"], channel["channel_id"], \
        "correct_and_valid_message") == {}
    # A message is buffered in the standup queue - Member
    owner = auth.auth_register("validcorrect@g.com", "valid_password", \
         "valid_correct_first_name", "valid_correct_last_name")
    channel = channel.channels_create(owner["token"], "Group Name", True)
    user = auth.auth_register("validcorrect1@g.com", "valid_password", \
        "valid_correct_first_name", "valid_correct_last_name")
    channel.channel_join(user["token"], channel["channel_id"])
    time = standup.standup_start(owner["token"], channel["channel_id"])
    assert standup.standup_send(user["token"], channel["channel_id"], \
        "correct_and_valid_message") == {}
    # Channel given does not exist
    with pytest.raises(ValueError, match = "Channel Does Not Exist"):
        user = auth.auth_register("validcorrect@g.com", "valid_password", \
            "valid_correct_first_name", "valid_correct_last_name")
        standup.standup_send(user["token"], 523523523, \
            "correct_and_valid_message")
    # The message sent was greater than max message length
    with pytest.raises(ValueError, match = "Message Too Long"):
        user = auth.auth_register("validcorrect@g.com", "valid_password", \
            "valid_correct_first_name", "valid_correct_last_name")
        channel = channel.channels_create(user["token"], "Group Name", True)
        time = standup.standup_start(user["token"], channel["channel_id"])
        standup.standup_send("valid_token", \
             "correct_and_valid_channel_with_standup", string_creator(1001))
    # User has not joined channel
    with pytest.raises(AccessError, match = "Cannot Access Channel"):
        owner = auth.auth_register("validcorrect@g.com", "valid_password", \
            "valid_correct_first_name", "valid_correct_last_name")
        channel = channel.channels_create(owner["token"], "Group Name", True)
        user = auth.auth_register("validcorrect1@g.com", "valid_password", \
            "valid_correct_first_name", "valid_correct_last_name")
        time = standup.standup_start(owner["token"], channel["channel_id"])
        standup.standup_send(user["token"], channel["channel_id"], \
                  "correct_and_valid_message")
    # Channel is not currently in standup mode
    with pytest.raises(AccessError, match = "Not Currently In Standup"):
        user = auth.auth_register("validcorrect@g.com", "valid_password", \
            "valid_correct_first_name", "valid_correct_last_name")
        channel = channel.channels_create(user["token"], "Group Name", True)
        standup.standup_send("valid_token", "correct_and_valid_channel", \
             "correct_and_valid_message")

# Creates a variable length string
def string_creator(length):
    string = ""
    for i in range(length):
        string += "a"
    return string
