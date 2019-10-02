import standup_functions as standup
import pytest
from Error import AccessError

def test_standup_start():
    with pytest.raises(ValueError, match = "Channel Does Not Exist"):
        standup.standup_start("valid_token", "incorrect_or_invalid_channel")
    with pytest.raises(AccessError, match = "Cannot Access Channel"):
        standup.standup_start("incorrect_or_invalid_token", "correct_and_valid_channel")
    
    assert standup.standup_start("valid_token", "correct_and_valid_channel") == 900 # Successful start

def test_standup_send():
    with pytest.raises(ValueError, match = "Channel Does Not Exist"):
        standup.standup_send("valid_token", "incorrect_or_invalid_channel_with_standup", "correct_and_valid_message") # Channel does not exist
    with pytest.raises(ValueError, match = "Message Too Long"):
        long_string = string_creator(1001)
        standup.standup_send("valid_token", "correct_and_valid_channel_with_standup", long_string) # Message too long
    with pytest.raises(AccessError, match = "Cannot Access Channel"):
        standup.standup_send("invalid_token", "correct_and_valid_channel_with_standup", "correct_and_valid_message") # User not apart of channel
    with pytest.raises(AccessError, match = "Not Currently In Standup"):
        standup.standup_send("valid_token", "correct_and_valid_channel", "correct_and_valid_message") # Not currently in standup

# Creates a variable length string
def string_creator(length):
    string = ""
    for i in range(length):
        string += "a"
    return string