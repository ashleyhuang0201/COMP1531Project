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
    For a given channel, start the standup period whereby for the next 15 minutes
    if someone calls "standup_send" with a message, it is buffered during the 15
    minute window then at the end of the 15 minute window a message will be added
    to the message queue in the channel from the user who started the standup.
    """

    channel = get_channel_by_channel_id(channel_id)
    user = get_user_by_token(token)
    if channel is None:
        raise ValueError("Channel Does Not Exist")
    if channel.in_standup:
        raise ValueError("Standup Already Running")
    if not channel.is_member(user.u_id):
        raise AccessError("Cannot Access Channel")

    # After 15 minutes call the channel.startupEnd method to collate all of the
    # startup contents
    channel.start_standup()
    Timer(length, channel.end_standup, args=[token]).start()
    time = datetime.datetime.now() + datetime.timedelta(minutes=15)

    return {"time" : time.timestamp()}

def standup_send(token, channel_id, message):
    """
    Sending a message to get buffered in the standup queue, assuming a standup
    is currently active
    """

    channel = get_channel_by_channel_id(channel_id)
    user = get_user_by_token(token)
    if channel is None:
        raise ValueError("Channel Does Not Exist")
    if len(message) > 1000:
        raise ValueError("Message Too Long")
    if not channel.is_member(user.u_id):
        raise AccessError("Cannot Access Channel")
    if not channel.in_standup:
        raise AccessError("Not Currently In Standup")

    channel.add_standup_message(token, message)

    return {}

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
    if channel.in_standup:
        channel.standup
    # If standup is not active
    return {
        "is_active" : False,
        "time_finish" : None
    }

    return {}
    return {"time" : time.timestamp()}

    { is_active, time_finish }