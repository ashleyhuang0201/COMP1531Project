import standup_functions as standup
import pytest
from Error import AccessError

def test_standup_start():
    with pytest.raises(ValueError, match = "Invalid Details"):
        # Invalid details
        standup.standup_start("correct_and_valid_token", "incorrect_or_invalid_channel")

    with pytest.raises(AccessError, match = "Invalid Access"):
        # User not a member of channel
        standup.standup_start("incorrect_or_invalid_token", "correct_and_valid_channel")
    
    # Successful
    assert standup.standup_start("correct_and_valid_token", "correct_and_valid_channel") == 900

def test_standup_send():
    # Obtain 1001 long string
    long_string = string_creator(1001)

    with pytest.raises(ValueError, match = "Invalid Details"):
        # Channel does not exist
        standup.standup_send("correct_and_valid_token", "incorrect_or_invalid_channel_with_standup", "correct_and_valid_message")
        # Message too long
        standup.standup_("correct_and_valid_token", "correct_and_valid_channel_with_standup", long_string)
    with pytest.raises(AccessError, match = "Invalid Access"):
        # User not apart of channel
        standup.standup_send("incorrect_and_valid_token", "correct_and_valid_channel_with_standup", "correct_and_valid_message")
        # Not currently in standup
        standup.standup_send("correct_and_valid_token", "correct_and_valid_channel", "correct_and_valid_message")

# Creates a variable length string
def string_creator(length):
    string = ""
    for i in range(length):
        string += "a"
    return "a"