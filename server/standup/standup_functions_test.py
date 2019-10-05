from server.standup import standup_functions as standup
import pytest
from server.helper.Error import AccessError

def test_standup_start():
    # A valid token and channel successfully starts a standup
    assert standup.standup_start("valid_token", \
        "correct_and_valid_channel") == 900
    # Channel id given does not exist
    with pytest.raises(ValueError, match = "Channel Does Not Exist"):
        standup.standup_start("valid_token", "incorrect_or_invalid_channel")
    # User has not joined the channel
    with pytest.raises(AccessError, match = "Cannot Access Channel"):
        standup.standup_start("incorrect_or_invalid_token", \
            "correct_and_valid_channel")

def test_standup_send():
    # A message is buffered in the standup queue
    assert standup.standup_send("valid_token", \
         "correct_and_valid_channel_with_standup", \
              "correct_and_valid_message") == {}
    # Channel given does not exist
    with pytest.raises(ValueError, match = "Channel Does Not Exist"):
        standup.standup_send("valid_token", \
             "incorrect_or_invalid_channel_with_standup", \
                  "correct_and_valid_message")
    # The message sent was greater than max message length
    with pytest.raises(ValueError, match = "Message Too Long"):
        standup.standup_send("valid_token", \
             "correct_and_valid_channel_with_standup", string_creator(1001))
    # User has not joined channel
    with pytest.raises(AccessError, match = "Cannot Access Channel"):
        standup.standup_send("invalid_token", \
             "correct_and_valid_channel_with_standup", \
                  "correct_and_valid_message")
    # Channel is not currently in standup mode
    with pytest.raises(AccessError, match = "Not Currently In Standup"):
        standup.standup_send("valid_token", "correct_and_valid_channel", \
             "correct_and_valid_message")


# Creates a variable length string
def string_creator(length):
    string = ""
    for i in range(length):
        string += "a"
    return string