'''
Test functions for standup_*
'''
import datetime as dt
import time

import pytest

import server.auth_functions as auth
import server.channel_functions as channel_func
import server.global_var as data
from server.Error import AccessError, ValueError
from server.standup_functions import (standup_active, standup_send,
                                      standup_start)


def test_standup_start():
    '''
    Test functions for standup_start
    '''
    data.initialise_all()

    # A valid token and channel successfully starts a standup - Owner
    owner = auth.auth_register("validcorrect@g.com", "valid_password", "a", "b")

    channel1 = channel_func.channels_create(owner["token"], "Owner", True)
    channel2 = channel_func.channels_create(owner["token"], "User", True)
    length = 1

    # Testing return time
    end_ex = get_standup_end(length)
    end_ac = standup_start(owner["token"], channel1["channel_id"], length)
    assert same_time(end_ex, end_ac["time_finish"])
    time.sleep(1)

    # A invalid token is used to access the function
    with pytest.raises(AccessError, match="Invalid token"):
        standup_start("123456", channel2["channel_id"], length)

    # A valid token and channel successfully starts a standup - User
    user = auth.auth_register("valid2@g.com", "valid_password", "a", "b")

    # User tries to start standup but has not joined the channel
    with pytest.raises(AccessError, match="Cannot Access Channel"):
        standup_start(user["token"], channel2["channel_id"], length)

    # User starts standup
    channel_func.channel_join(user["token"], channel2["channel_id"])
    end_ex = get_standup_end(length)
    end_ac = standup_start(user["token"], channel2["channel_id"], length)
    assert same_time(end_ex, end_ac["time_finish"])

    # Channel id given does not exist
    with pytest.raises(ValueError, match="Channel Does Not Exist"):
        standup_start(user["token"], 21512512521512, length)

    # Start standup when already running
    with pytest.raises(ValueError, match="Standup Already Running"):
        standup_start(user["token"], channel2["channel_id"], length)

    # Standup works on private channel
    private = channel_func.channels_create(owner["token"], "Owner", False)
    end_ex = get_standup_end(length)
    end_ac = standup_start(owner["token"], private["channel_id"], length)
    assert same_time(end_ex, end_ac["time_finish"])
    time.sleep(1)

def test_standup_send():

    '''
    Test functions for standup_send
    '''

    data.initialise_all()

    # A message is buffered in the standup queue - Owner
    owner = auth.auth_register("validcorrect@g.com", "valid_password", "a", "b")

    channel = channel_func.channels_create(owner["token"], "Owner", True)

    length = 2

    # Channel is not currently in standup mode
    with pytest.raises(ValueError, match="Not Currently In Standup"):
        standup_send(owner["token"], channel["channel_id"], \
             "correct_and_valid_message")

    standup_start(owner["token"], channel["channel_id"], length)

    assert standup_send(owner["token"], channel["channel_id"], \
        "correct_and_valid_message") == {}

    # A invalid token is used to access the function
    with pytest.raises(AccessError, match="Invalid token"):
        standup_send("123456", channel["channel_id"], length)

    user = auth.auth_register("validcorrect1@g.com", "valid_password", "a", "b")

    # User tries to send message but has not joined channel
    with pytest.raises(AccessError, match="Cannot Access Channel"):
        standup_send(user["token"], channel["channel_id"], \
        "correct_and_valid_message")

    # A message is buffered in the standup queue - Member
    channel_func.channel_join(user["token"], channel["channel_id"])
    assert standup_send(user["token"], channel["channel_id"], \
        "correct_and_valid_message") == {}

    # Channel given does not exist
    with pytest.raises(ValueError, match="Channel Does Not Exist"):
        standup_send(user["token"], 523523523, \
            "correct_and_valid_message")

    # The message sent was greater than max message length
    with pytest.raises(ValueError, match="Message Too Long"):
        long_string = "a" * 1001
        standup_send(user["token"], channel["channel_id"], long_string)

    # Check still works in private channel
    private = channel_func.channels_create(owner["token"], "Owner", False)
    standup_start(owner["token"], private["channel_id"], length)
    assert standup_send(owner["token"], private["channel_id"], \
        "correct_and_valid_message") == {}

    time.sleep(2)

def test_standup_active():
    '''
    Test functions for standup_active
    '''

    data.initialise_all()

    # A message is buffered in the standup queue - Owner
    owner = auth.auth_register("validcorrect@g.com", "valid_password", "a", "b")

    channel = channel_func.channels_create(owner["token"], "Owner", True)

    # A invalid token is used to access the function
    with pytest.raises(AccessError, match="Invalid token"):
        standup_active("123456", channel["channel_id"])

    # Channel given does not exist
    with pytest.raises(ValueError, match="Channel Does Not Exist"):
        standup_active(owner["token"], -1)

    # Not in standup
    assert standup_active(owner["token"], channel["channel_id"]) == {
            "is_active": False,
            "time_finish": None
        }

    # In standup
    length = 1
    standup = standup_start(owner["token"], channel["channel_id"], length)
    assert standup_active(owner["token"], channel["channel_id"]) == {
        "is_active": True,
        "time_finish": standup['time_finish']
    }

    time.sleep(1)

def get_standup_end(length):
    '''
    Get the time that standup ends
    '''
    return dt.datetime.now().timestamp() + length

def same_time(expected_time, actual_time):
    '''
    Check that standup end time expected and actual are within 1 second of
    each other
    '''
    return expected_time - actual_time < 1
