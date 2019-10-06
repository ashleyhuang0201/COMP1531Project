# General

Passwords can be of infinite length

First and last name are less than 50 characters and can include any characters

A channel is not destroyed if the last user leaves the channel

The database structure that will be used in iteration 1 will be accessable via helper functions

# auth function assumptions

## auth_login

Users will enter emails (correct, invalid, not registered) and passwords (correct, incorrect)

Users will not enter emails (incorrrect) and passwords (invalid)

Multiple users can login using the same account at the same time

## auth_logout

Users will enter tokens (valid, invalid)

## auth_register

Users will enter emails (invalid, already registered, correct), passwords (invalid, valid), first name (invalid, valid) and last name (valid, invalid)

Users are logged straight after registering an account

Each email address may only be used by 1 user

## auth_passwordreset_request

Users will enter email (incorrect, correct, invalid, valid)

Assume that the code that is emailed is saved in the database for access

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

A user can remove themself as a owner. If the user was the last owner, the channel now has no owners

## channeLs_list

The function will be called with a token

## channls_listall

The function will be called with a token

## channels_create

The function will be called with a token, a name and a public/private boolean

Assume that no messages are in the channel upon its creation

# message function assumptions

## message_sendlater

The function will be called with a token, a channel id, a message, and a time to be sent

The channel based on ID will not be deleted in the time till the message is to be sent

## message_send

The function will be called with a token, a channel id and a message

Assume that message is only send if there is a message to send

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

Assume that without error the message is successfully pinned

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

The function will be called with a token and a query string  \
The function is expected to return a list in order of most recent messages matching the query where the most recent message is at index 0  
The function is expected to search all channels for query string

# admin_userpermission_change

The function will be called with a token, user id and a permission id
