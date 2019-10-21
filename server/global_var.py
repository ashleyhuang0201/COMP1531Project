import datetime

#Single global variable containing nested dictionaries/lists
data = {
    "users": [],
    "tokens": [],
    "channels": [],
    "owner": [],
    "messages": [],
}

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
        A member of slackr is a member in channels they are not owners of and an owner in channels they are owners of # 3
        """
    
    def change_permissions(self, permission_id):
        self.permission = permission_id

class Channel:
    def __init__(self, name, isPublic):
        self.name = name
        self.id = len(data["channels"]) + 1

        # A list of dictionaries containing {message_id, u_id, message, 
        # time_created, is_unread, reacts, is_pinned }
        self.messages = [] 

        # A list of dictionaries containing messages 
        # {(message_id, message, u_id, time_created) and send time}
        self.send_later = [] 

        self.owners = []
        self.users = []
        self.isPublic = isPublic

    def send_message(self, message):
        # To do
        pass

    def send_later(self, message, token, time_sent):
        # Message id starts from 0 index in messages?
        message_id = len(self.send_later) + len(self.messages)
        self.send_later.append({
            "message_id": message_id,
            "message": message,
            "u_id": token,
            "time_created": time_sent,
        })
        return {"message_id": message_id}

    def update_send_later(self, message):
        # Checks if it is possible to send message
        # To be placed in its proper location
        now = datetime.datetime.now()
        for item in self.send_later:
            if (now - item["time_created"]).total_seconds() >= item["send_time"]:
                # Implement transfer from send_later to maessages once channel object is better defined
                pass

    def user_in_channel(token):a
        # Checks if a user is in the channel

    def search_message(self, substring):
        # Checks messages for if substring exists
        # Returns strings as a list

    def add_react(self, message_id, react_id):
        # To do
        pass
    def remove_react(self, message_id, react_id):
        # To do
        pass
    def edit_message(self, message_id, message):
        # Implement after confirmation
        pass
    def remove_message(self, message_id):
        # Implement after confirmation
        pass
    def unpin_message(self, message_id):
        # To do
        pass
    def pin_message(self, message_id):
        # Implement
        pass
    def add_owner(self):
        pass
    def remove_owner(self):
        pass

    def add_user(self, u_id):
        self.users.append(u_id)

    def remove_user(self):
        pass
