# General
Passwords can be of infinite length

First and last name are less than 50 characters and can include any characters


# auth function assumptions
## auth_login
Users will enter emails (correct, invalid, not registered) and passwords (correct, incorrect)

Users will not enter emails (incorrrect) and passwords (invalid)

Multiple users can login using the same account at the same time
## auth_logout
Users will enter tokens (valid, invalid)
## auth_register
Users will enter emails (invalid, already registered, correct), passwords (invalid, valid), first name (invalid, valid) and last name (valid, invalid)
## auth_passwordreset_request
Users will enter email (incorrect, correct, invalid, valid)
## auth_passwordreset_reset
Users will enter reset code (valid, invalid) and password (invalid, valid)


# channel function assumption
## channel_invite
The function will be called with a token, channel id and a user id
## channel_details
The function will be called with a token and a channel id
## channel_messages
The function will be called with a token, channel id and a start
## channel_leave
The function will be called with a token and a channel id
## channel_join
The function will be called with a token and a channel id
## channel_addowner
The function will be called with a token, a channel id and a user id
## channel_removeowner
The function will be called with a token, a channel id and a user id
## channeLs_list
The function will be called with a token
## channls_listall
The function will be called with a token
## channels_create
The function will be called with a token, a name and a public/private boolean


# message function assumptions
## message_sendlater
The function will be called with a token, a channel id, a message, and a time to be sent

The channel based on ID will not be deleted in the time till the message is to be sent
## message_send
The function will be called with a token, a channel id and a message
## message_remove
The function will be called with a token and a message id
## message_edit
The function will be called with a token, a message_id and a new message
## message_react
The function will be called with a token, a message id and a react id
## message_unreact
The function will be called with a token, a message id and a react id
## message_pin
The function will be called with a token and a message id
## message_unpin
The function will be called with a token and a message id


# user function assumptions
## user_profile
The function will be called with a token and a user id
## user_profile_setname
The function will be called with a token, a first name and a last name
## user_profile_setemail
The function will be called with a token and an email
## user_profile_sethandle
The function will be called with a token and a handle
## user_proviles_uploadphoto
The function will be called with a token, image url and crop co-ordinates


# standup assumptions
## standup_start
Users will try start on channel ((non-existant, existing) and (apart of, not apart of))
## standup_send
Users will try to send on channel ((non-existant, existing) and (apart of, not apart of) and (standup time running, standup time stopped)), message (longer than 1000 characters, less than or equal to 1000)

## Misc
# search
The function will be called with a token and a query string
# admin_userpermission_change
The function will be called with a token, user id and a permission id