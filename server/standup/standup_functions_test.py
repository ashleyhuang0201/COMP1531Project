from server.standup import standup_functions as standup
from server.auth import auth_functions as auth
import pytest
from server.helper.Error import AccessError
from server.channel import channel_functions as channel_func

def test_standup_start():
    # A valid token and channel successfully starts a standup - Owner
    owner = auth.auth_register("validcorrect@g.com", "valid_password", \
         "valid_correct_first_name", "valid_correct_last_name")
    
    channel1 = channel_func.channels_create(owner["token"], "Owner", True)
    
    assert standup.standup_start(owner["token"], channel1["channel_id"]) \
        == {"time": get_standup_end()}

    # A valid token and channel successfully starts a standup - User
    user = auth.auth_register("validcorrect@g.com", "valid_password", \
         "valid_correct_first_name", "valid_correct_last_name")
    
    channel2 = channel_func.channels_create(user["token"], "User", True)
    
    assert standup.standup_start(user["token"], channel2["channel_id"]) \
        == {"time": get_standup_end()}

    # Channel id given does not exist
    with pytest.raises(ValueError, match = "Channel Does Not Exist"):
        standup.standup_start(user["token"], 21512512521512)

    # User has not joined the channel
    with pytest.raises(AccessError, match = "Cannot Access Channel"):
        user2 = auth.auth_register("validcorrect2@g.com", "valid_password", \
            "valid_correct_first_name", "valid_correct_last_name")
        
        standup.standup_start(user2["token"], channel1["channel_id"])

def test_standup_send():
    # A message is buffered in the standup queue - Owner
    owner = auth.auth_register("validcorrect@g.com", "valid_password", \
         "valid_correct_first_name", "valid_correct_last_name")
    
    channel = channel_func.channels_create(owner["token"], "Owner", True)
    
    standup.standup_start(owner["token"], channel["channel_id"])
    
    assert standup.standup_send(owner["token"], channel["channel_id"], \
        "correct_and_valid_message") == {}

    # A message is buffered in the standup queue - Member
    user = auth.auth_register("validcorrect1@g.com", "valid_password", \
         "valid_correct_first_name", "valid_correct_last_name")
    
    assert standup.standup_send(user["token"], channel["channel_id"], \
        "correct_and_valid_message") == {}

    # Channel given does not exist
    with pytest.raises(ValueError, match = "Channel Does Not Exist"):
        standup.standup_send(user["token"], 523523523, \
            "correct_and_valid_message")

    # The message sent was greater than max message length
    with pytest.raises(ValueError, match = "Message Too Long"):
        standup.standup_send("valid_token", \
             "correct_and_valid_channel_with_standup", string_creator(1001))

    # User has not joined channel
    with pytest.raises(AccessError, match = "Cannot Access Channel"):
        user2 = auth.auth_register("validcorrect2@g.com", "valid_password", \
            "valid_correct_first_name", "valid_correct_last_name")
        
        standup.standup_send(user2["token"], channel["channel_id"], \
                  "correct_and_valid_message")

    # Channel is not currently in standup mode
    with pytest.raises(AccessError, match = "Not Currently In Standup"):
        channel2 = channel_func.channels_create(user["token"], "Group", True)
        standup.standup_send(user["token"], channel2["channel_id"], \
             "correct_and_valid_message")

# Creates a variable length string
def string_creator(length):
    string = ""
    for i in range(length):
        string += "a"
    return string

# returns expected end time of standup (15 mins in future)
def get_standup_end():
    return 900