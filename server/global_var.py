'''
File for all global variables, classes and functions
'''
import datetime
import hashlib
import random
import os
from flask import request

import server.helpers as helpers
import server.message_functions as msg
from server.constants import LIKE_REACT, LIKE_REACT_INDEX, SLACKR_USER, \
    DEFAULT_PIC

# Dictionary list containing all global data
data = {
    "users": [],
    "tokens": [],
    "channels": [],
    "reset_code": [],
}

# jwt secret
SECRET = "token_hash"

# global message id
message_id_ticker = 0

# Resets all global data to initial state
def initialise_all():
    global data
    global message_id_ticker

    data = {
        "users": [],
        "tokens": [],
        "channels": [],
        "reset_code": [],
    }

    message_id_ticker = 0

''' Object class for storing an user's data '''
class User:
    def __init__(self, u_id, email, password, name_first, name_last):
        self.u_id = u_id
        self.email = email
        self.password = password
        self.name_first = name_first
        self.name_last = name_last
        self.handle = helpers.generate_handle(name_first, name_last, u_id)
        self.permission = SLACKR_USER
        try:
            url = request.host_url
        except:
            url = "http://localhost:5001/"
        self.has_photo = f"{url}imgurl/{DEFAULT_PIC}"


    # Change permission of user
    def change_permissions(self, permission_id):
        self.permission = permission_id

    # Change password
    def change_password(self, new_password):
        self.password = hashlib.sha256(new_password.encode()).hexdigest()

    # Updating user's first name
    def update_name_first(self, name_first):
        self.name_first = name_first

    # Updating user's last name
    def update_name_last(self, name_last):
        self.name_last = name_last

    # Updating user's email
    def update_email(self, email):
        self.email = email

    # Updating user's handle
    def update_handle(self, handle_str):
        self.handle = handle_str

    # Uploads a photo
    def upload_photo(self, img_addr):
        # Remove old photo and upload new one
        if self.has_photo:
            index = self.has_photo.rfind("/")
            if self.has_photo[index:] != "/default.jpg":
                os.remove(f"server/assets/images{self.has_photo[index:]}")
        self.has_photo = f"{img_addr}"

    # Removes a photo
    def remove_photo(self):
        self.has_photo = None

''' Object class for storing a message's data '''
class Message:
    def __init__(self, u_id, message, channel_id):
        global message_id_ticker
        self.id = message_id_ticker
        message_id_ticker += 1
        self.sender = u_id
        self.message = message
        self.channel = channel_id
        self.time_created = datetime.datetime.now().timestamp()
        self.reacts = [{"react_id": LIKE_REACT, "u_ids": []}]
        self.is_pinned = False

    # Checks if u_id was the sender of the message
    def user_sent_message(self, u_id):
        if self.sender == u_id:
            return True
        else:
            return False

    # Checks if u_id is currently reacted to the message
    def user_has_reacted(self, u_id, react_id):
        for react in self.reacts:
            if react["react_id"] == react_id:
                if u_id in react["u_ids"]:
                    return True
                else:
                    return False

    # Edits the message of the message object
    def edit_message(self, message):
        self.message = message

    # Adds a reaction to the message
    def add_react(self, u_id, react_id):
        for react in self.reacts:
            if react["react_id"] == react_id:
                react["u_ids"].append(u_id)

    # Remove a reaction to the message
    def remove_react(self, u_id, react_id):
        for react in self.reacts:
            if react["react_id"] == react_id:
                react["u_ids"].remove(u_id)

    # Sets a message to be pinned
    def pin_message(self):
        self.is_pinned = True

    # Unpins a message
    def unpin_message(self):
        self.is_pinned = False

''' Object class for storing a channel's data '''
class Channel:
    def __init__(self, name, u_id, is_public):
        self.name = name
        self.id = len(data["channels"])
        self.messages = []
        self.owners = []
        self.users = []
        self.is_public = is_public
        self.in_standup = False
        self.standup_end = None
        self.standup_messages = []
        self.add_owner(u_id)
        self.add_user(u_id)

    # Adds a member to the channel
    def add_user(self, u_id):
        user = helpers.get_user_by_u_id(u_id)
        self.users.append(user)

    # Removes a member from the channel
    def remove_user(self, u_id):
        for user in self.users:
            if user.u_id == u_id:
                self.users.remove(user)

    # Adds an owner to the channels
    def add_owner(self, u_id):
        user = helpers.get_user_by_u_id(u_id)
        self.owners.append(user)

    # Removes an owner from the channel
    def remove_owner(self, u_id):
        for user in self.owners:
            if user.u_id == u_id:
                self.owners.remove(user)

    # Checks if an user is a member
    def is_member(self, u_id):
        for user in self.users:
            if user.u_id == u_id:
                return True
        return False

    # Checks if an user is a owner
    def is_owner(self, u_id):
        for user in self.owners:
            if user.u_id == u_id:
                return True
        return False

    # Returns a list of dictionaries containing information for channel_details
    def get_members_details(self):
        members = []
        for user in self.users:
            members.append({"u_id": user.u_id, "name_first": user.name_first, \
                 "name_last": user.name_last, \
                      "profile_img_url": user.has_photo})
        return members

    # Returns a list of dictionaries containing information for channel_details
    def get_owners_details(self):
        owners = []
        for user in self.owners:
            owners.append({"u_id": user.u_id, "name_first": user.name_first, \
                 "name_last": user.name_last, \
                      "profile_img_url": user.has_photo})
        return owners

    # Adds a message to the channel (New messages are at the front)
    def add_message(self, message):
        self.messages.insert(0, message)

    # Removes a message from the channel
    def remove_message(self, message_id):
        for message in self.messages:
            if message_id == message.id:
                self.messages.remove(message)

    # Searches for a message given a substring
    def search_message(self, token, substring):
        '''
        Given a query string, return a list of messages in the channel
        '''

        messages = []

        # Checking all messages in channel
        for message in self.messages:
            # If message contains substring
            if (message.message).find(str(substring)) != -1:
                # Returning message
                reacts = message.reacts
                reacts[LIKE_REACT_INDEX]["is_this_user_reacted"] = \
                message.user_has_reacted(helpers.decode_token(token), LIKE_REACT)

                # Append message dictionary into list
                messages.append({
                    "message_id": message.id,
                    "u_id": message.sender,
                    "message": message.message,
                    "time_created": message.time_created,
                    "reacts": reacts,
                    "is_pinned": message.is_pinned,
                })

        return messages

    def update_message_object(self, message_id, message_object):
        for message in self.messages:
            if message_id == message.id:
                message.message = message_object.message
                message.reacts = message_object.reacts
                message.is_pinned = message_object.is_pinned

    def start_standup(self, standup_end):
        self.in_standup = True
        self.standup_end = standup_end

    def end_standup(self, token):
        self.in_standup = False
        self.standup_end = None
        message = ""
        for m in self.standup_messages:
            line = ': '.join([m['user'], m['message']])
            message = '\n'.join([message, line])
        self.standup_messages = []
        msg.message_send(token, self.id, message)

    def add_standup_message(self, token, message):
        self.standup_messages.append({
            'user': helpers.get_user_by_token(token).handle,
            'message': message
        })

    def user_in_channel(self, u_id):
        if self.is_member(u_id) or self.is_owner(u_id):
            return True
        # No such user
        return False

    def standup_running(self):
        if self.in_standup:
            return True
        return False

    def get_standup_end(self):
        return self.standup_end