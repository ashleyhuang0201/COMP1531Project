# General

Passwords can be of infinite length

First and last name are less than 50 characters and can include any characters

A channel is not destroyed if the last user leaves the channel

The database structure that will be used in iteration 1 will be accessable via helper functions

# auth function assumptions

## auth_login

The function will be called with a email and password

Multiple active sessions can be associated with a single account

## auth_logout

The function will be called with a token

## auth_register

The function will be called with an email, password, first name and last name

Users are logged straight after registering an account

Each email address can only be used by one user

## auth_passwordreset_request

The function will be called with an email

Assume that the code that is emailed is saved in the database for access

## auth_passwordreset_reset

The function will be called with a reset code and password

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

Slackr owners is also an owner of the channels

## channel_removeowner

The function will be called with a token, a channel id and a user id

A user can remove themself as a owner. If the user was the last owner, the channel now has no owners

Slackr owners is also an owner of the channels

## channels_list

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

Assume that message ID will be retrievable from the database after it has been sent

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

The function will be called with a token and a channel

Function will do nothing if standup has already started and user attempts (correctly) to start a standup

## standup_send
The function will be called with a token, channel and a message

## Misc

# search

The function will be called with a token and a query string  \
The function is expected to return a list in order of most recent messages matching the query where the most recent message is at index 0  
The function is expected to search all channels for query string

# admin_userpermission_change

The function will be called with a token, user id and a permission id
