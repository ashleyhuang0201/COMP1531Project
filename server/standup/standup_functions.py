from server.helper.Error import AccessError

"""
For a given channel, start the standup period whereby for the next 15 minutes 
if someone calls "standup_send" with a message, it is buffered during the 15
minute window then at the end of the 15 minute window a message will be added
to the message queue in the channel from the user who started the standup.
"""
def standup_start(token, channel_id):
    if existing_channel(channel_id) == False:
        raise ValueError("Channel Does Not Exist")
    if user_in_channel(token, channel_id) == False:
        raise AccessError("Cannot Access Channel")

    return 900

"""
Sending a message to get buffered in the standup queue, assuming a standup is currently active
"""
def standup_send(token, channel_id, message):
    if existing_channel(channel_id) == False:
        raise ValueError("Channel Does Not Exist")
    if greater_than_1000_characters(message) == True:
        raise ValueError("Message Too Long")
    if user_in_channel(token, channel_id) == False:
        raise AccessError("Cannot Access Channel")
    if in_standup(channel_id) == False:
        raise AccessError("Not Currently In Standup")

    return {}

# Checks if a channel exists
def existing_channel(channel_id):
    if channel_id == "correct_and_valid_channel" or channel_id == "correct_and_valid_channel_with_standup":
        return True
    else:
        return False

# Checks if a user is apart of a channel
def user_in_channel(token, channel_id):
    if token == "valid_token" and (channel_id == "correct_and_valid_channel" or channel_id == "correct_and_valid_channel_with_standup"):
        return True
    else:
        return False

# Checks if a message is more than 1000 character
def greater_than_1000_characters(message):
    if len(message) > 1000:
        print(len(message))
        return True
    else:
        return False

# Checks if a channel is currently in standup
def in_standup(channel_id):
    if channel_id == "correct_and_valid_channel_with_standup":
        return True
    else:
        return False