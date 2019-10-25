from threading import Timer
import datetime
from server.Error import AccessError
import server.global_var as data
from server.helpers import get_channel, get_user_by_token


"""
For a given channel, start the standup period whereby for the next 15 minutes 
if someone calls "standup_send" with a message, it is buffered during the 15
minute window then at the end of the 15 minute window a message will be added
to the message queue in the channel from the user who started the standup.
"""
def standup_start(token, channel_id):
    channel = get_channel(channel_id)
    user = get_user_by_token(token)
    if channel == None:
        raise ValueError("Channel Does Not Exist")
    if channel.inStandup:
        raise ValueError("Standup Already Running")
    if not channel.is_member(user.id):
        raise AccessError("Cannot Access Channel")

    # After 15 minutes call the channel.startupEnd method to collate all of the
    # startup contents
    Timer(15 * 60, channel.startupEnd)
    time = datetime.datetime.now() + datetime.timedelta(minutes=15)

    return {"time" : time.timestamp()}

"""
Sending a message to get buffered in the standup queue, assuming a standup 
is currently active
"""
def standup_send(token, channel_id, message):
    channel = get_channel(channel_id)
    user = get_user_by_token(token)
    if channel == None:
        raise ValueError("Channel Does Not Exist")
    if len(message) > 1000:
        raise ValueError("Message Too Long")
    if not channel.is_member(user.id):
        raise AccessError("Cannot Access Channel")
    if not channel.inStandup():
        raise AccessError("Not Currently In Standup")

    channel.addStandupMessage(token, message)

    return {}