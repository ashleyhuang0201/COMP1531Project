'''
Standup Functions
'''
from threading import Timer
import datetime
from server.Error import AccessError
import server.global_var as data
from server.helpers import get_channel_by_channel_id, get_user_by_token

def standup_start(token, channel_id, length):
    """
    For a given channel, start the standup period whereby for the next "length"
    seconds if someone calls "standup_send" with a message, it is buffered
    during the X second window then at the end of the X second window a message
    will be added to the message queue in the channel from the user who started
    the standup. X is an integer that denotes the number of seconds that the
    standup occurs for
    """

    # Invalid user has accessed function
    if not helpers.valid_token(token):
        raise AccessError("Invalid token")

    channel = get_channel_by_channel_id(channel_id)
    user = get_user_by_token(token)

    if channel is None:
        raise ValueError("Channel Does Not Exist")
    if channel.in_standup is not False:
        raise ValueError("Standup Already Running")
    if not channel.is_member(user.u_id):
        raise AccessError("Cannot Access Channel")

    # Start standup and after length seconds end the standup
    channel.start_standup(length)
    Timer(length, channel.end_standup, args=[token]).start()
    time = datetime.datetime.now() + datetime.timedelta(seconds=length)

    return {"time" : time.timestamp()}

def standup_send(token, channel_id, message):
    """
    Sending a message to get buffered in the standup queue, assuming a standup
    is currently active
    """

    # Invalid user has accessed function
    if not helpers.valid_token(token):
        raise AccessError("Invalid token")

    channel = get_channel_by_channel_id(channel_id)
    user = get_user_by_token(token)

    if channel is None:
        raise ValueError("Channel Does Not Exist")
    if len(message) > 1000:
        raise ValueError("Message Too Long")
    if not channel.is_member(user.u_id):
        raise AccessError("Cannot Access Channel")
    if channel.in_standup is False:
        raise ValueError("Not Currently In Standup")

    channel.add_standup_message(token, message)

    return {}

def standup_active(token, channel_id):
    '''
    For a given channel, return whether a standup is active in it, and what
    time the standup finishes. If no standup is active, then time_finish
    returns None
    '''

    # Invalid user has accessed function
    if not helpers.valid_token(token):
        raise AccessError("Invalid token")

    channel = get_channel_by_channel_id(channel_id)

    # Checking if channel exists
    if channel is None:
        raise ValueError("Channel Does Not Exist")

    if channel.in_standup is not False:
        # If channel is active
        return {
            "is_active": True,
            "time_finish": channel.time_left_standup()
        }
    # Channel is not active
    return {
        "is_active": False,
        "time_finish": None
    }

