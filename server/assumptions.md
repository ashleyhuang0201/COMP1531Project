# General
Passwords can be of infinite length

First and last name are less than 50 characters and can include any characters

# auth_login
Users will enter emails (correct, invalid, not registered) and passwords (correct, incorrect)

Users will not enter emails (incorrrect) and passwords (invalid)

# auth_logout
Users will enter tokens (valid, invalid)

# auth_register
Users will enter emails (invalid, already registered, correct), passwords (invalid, valid), first name (invalid, valid) and last name (valid, invalid)

# auth_passwordreset_request
Users will enter email (incorrect, correct, invalid, valid)

# auth_passwordreset_reset
Users will enter reset code (valid, invalid) and password (invalid, valid)

# message functions assumptions
## message_sendlater
The function will be called with a token, a channel id, a message, and a time to be sent
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


# standup_start
Users will try start on channel ((non-existant, existing) and (apart of, not apart of))

# standup_send
Users will try to send on channel ((non-existant, existing) and (apart of, not apart of) and (standup time running, standup time stopped)), message (longer than 1000 characters, less than or equal to 1000)