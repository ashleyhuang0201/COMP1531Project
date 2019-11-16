'''
Standup Functions
'''
from threading import Timer
import datetime

from server.Error import AccessError, ValueError
import server.global_var as data
from server.helpers import get_channel_by_channel_id, get_user_by_token, \
     valid_token
from server.constants import MAX_MESSAGE_LENGTH

@valid_token
def standup_start(token, channel_id, length):
    '''
    For a given channel, start the standup period whereby for the next "length"
    seconds if someone calls "standup_send" with a message, it is buffered
    during the X second window then at the end of the X second window a message
    will be added to the message queue in the channel from the user who started
    the standup. X is an integer that denotes the number of seconds that the
    standup occurs for
    '''

    channel = get_channel_by_channel_id(channel_id)
    user = get_user_by_token(token)

    if channel is None:
        raise ValueError("Channel Does Not Exist")
    if channel.standup_running() is not False:
        raise ValueError("Standup Already Running")
    if not channel.is_member(user.u_id):
        raise AccessError("Cannot Access Channel")

    # Start standup and after length seconds end the standup
    time = datetime.datetime.now() + datetime.timedelta(seconds=length)
    channel.start_standup(time.timestamp())
    Timer(length, channel.end_standup, args=[token]).start()

    return {"time_finish" : time.timestamp()}

@valid_token
def standup_send(token, channel_id, message):
    '''
    Sending a message to get buffered in the standup queue, assuming a standup
    is currently active
    '''

    channel = get_channel_by_channel_id(channel_id)
    user = get_user_by_token(token)

    if channel is None:
        raise ValueError("Channel Does Not Exist")
    if len(message) > MAX_MESSAGE_LENGTH:
        raise ValueError("Message Too Long")
    if not channel.is_member(user.u_id):
        raise AccessError("Cannot Access Channel")
    if channel.standup_running() is False:
        raise ValueError("Not Currently In Standup")

    channel.add_standup_message(token, message)

    return {}

@valid_token
def standup_active(token, channel_id):
    '''
    For a given channel, return whether a standup is active in it, and what
    time the standup finishes. If no standup is active, then time_finish
    returns None
    '''

    channel = get_channel_by_channel_id(channel_id)

    # Checking if channel exists
    if channel is None:
        raise ValueError("Channel Does Not Exist")

    # If standup is active
    if channel.standup_running():
        return {
            "is_active": True,
            "time_finish": channel.get_standup_end()
        }
    # Standup is not active
    return {
        "is_active": False,
        "time_finish": None
    }
