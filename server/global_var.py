import datetime
from server.message_functions import message_send
from server.helpers import get_user

#Single global variable containing nested dictionaries/lists
data = {
    "users": [],
    "tokens": [],
    "channels": [],
    "messages": [],
    "reset_code": [],
}

message_id_ticker = 0

class User:
    def __init__(self, u_id, email, password, name_first, name_last):
        self.u_id = u_id
        self.email = email
        self.password = password
        self.name_first = name_first
        self.name_last = name_last
        self.handle = f"{name_first}{name_last}"
        self.permission = 3
        """
        An owner of slackr is an owner in every channel # 1
        An admin of slackr is an owner in every channel # 2
        A member of slackr is a member in channels they are not owners of
        and an owner in channels they are owners of # 3
        """

    def change_permissions(self, permission_id):
        self.permission = permission_id

    def update_name_first(self, name_first):
        self.name_first = name_first

    def update_name_last(self, name_last):
        self.name_last = name_last

    def update_email(self, email):
        self.email = email

    def update_handle(self, handle_str):
        self.handle = handle_str

class Message:
    def __init__(self, u_id, message, channel_id):
        self.id = message_id_ticker
        message_id_ticker += 1
        self.sender = u_id
        self.message = message
        self.channel = channel_id
        self.time_created = datetime.datetime.now
        self.reacts = [{"react_id": 1, "u_id": []}]
        self.is_pinned = False

    def user_sent_message(self, u_id):
        if self.sender == u_id:
            return True
        else:
            return False

    def user_has_reacted(self, u_id):
        for react in channel.reacts:
            if react["react_id"] == 1:
                if u_id in react["u_id"]:
                    return True
                else:
                    return False

    def update_message(self, message):
        self.message = message

    def add_react(self, u_id):
        for react in channel.reacts:
            if react["react_id"] == 1:
                react["u_id"].append(u_id)

    def remove_react(self, u_id):
        for react in channel.reacts:
            if react["react_id"] == 1:
                react["u_id"].remove(u_id)

    def pin_message(self):
        self.is_pinned = True

    def unpin_message(self):
        self.is_pinned = False


class Channel:
    def __init__(self, name, u_id, is_public):
        self.name = name
        self.id = len(data["channels"])
        # messages: a list of message objects
        self.messages = []
        #send_later: a list of dictionaries containing messages and a send time
        self.send_later = []
        self.owners = [u_id]
        self.users = [u_id]
        self.is_public = is_public
        self.in_standup = False
        self.standup_messages = []

    def add_user(self, u_id):
        self.users.append(u_id)

    def remove_user(self, u_id):
        self.users.remove(u_id)

    def add_owner(self, u_id):
        self.owners.append(u_id)

    def remove_owner(self, u_id):
        self.owners.remove(u_id)

    def is_member(self, u_id):
        if u_id in self.users:
            return True
        else:
            return False

    def is_public(self):
        if self.is_public == True:
            return True
        else:
            return False

    def add_message(self, message):
        self.messages.append(message)

    def remove_message(self, message_id):
        for message in self.messages:
            if message_id == message.id:
                removed_message = message

        self.messages.remove(removed_message)

    def update_message_object(self, message_id, message_object):
        for message in self.messages:
            if message_id == message.id:
                message.message = message_object.message
                message.reacts = message_object.reacts
                message.is_pinned = message_object.is_pinned

    def start_standup(self):
        self.in_standup = True

    def end_standup(self, token):
        self.in_standup = False
        message = ""
        for m in self.standup_messages:
            line = ': '.join(m['user'], m['message'])
            '\n'.join(message, line)
        self.standup_messages = []
        message_send(token, self.id, message)

    def add_standup_message(self, token, message):
        self.standup_messages.append({'user': get_user(token).handle, 'message': message})
