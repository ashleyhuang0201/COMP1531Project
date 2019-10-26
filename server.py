"""Flask server"""
import sys
from json import dumps
from flask import Flask, request

from server import global_var
from server import auth_functions as auth
from server import channel_functions as channel
from server import user_functions as user
from server import standup_functions as standup
from server import message_functions as message
from server import search_function as Search
from server import admin_userpermission_change_function as permission

APP = Flask(__name__)


@APP.route('/echo/get', methods=['GET'])
def echo1():
    """ Description of function """
    return dumps({
        'echo' : request.args.get('echo'),
    })

@APP.route('/echo/post', methods=['POST'])
def echo2():
    """ Description of function """
    return dumps({
        'echo' : request.form.get('echo'),
    })

@APP.route('/auth/login', methods=['POST'])
def auth_login():
    """
    Given a registered user' email and password, generates a valid token
    for the user to remain authenticated
    """
    #Gets username and password
    email = request.form.get("email")
    password = request.form.get("password")

    #Calls function from auth_functions.py
    return dumps(
        auth.auth_login(email, password)
    )

@APP.route('/auth/logout', methods=['POST'])
def auth_logout():
    """ Given an active token, invalidates the token to log the user out """
    token = request.form.get("token")
    return dumps(
        auth.auth_logout(token)
    )

@APP.route('/auth/register', methods=['POST'])
def auth_register():
    """
    Given a user's details, creates a new account and returns a new token
    """
    #Gets user details
    email = request.form.get("email")
    password = request.form.get("password")
    name_first = request.form.get("name_first")
    name_last = request.form.get("name_last")

    return dumps(
        auth.auth_register(email, password, name_first, name_last)
    )

@APP.route('/auth/passwordreset/request', methods=['POST'])
def auth_passwordreset_request():
    """ 
    Given an email address, if the user is a registered user, sends an email 
    with a code that when entered into auth_passwordreset_reset authorises the 
    user to change their password 
    """

    email = request.form.get("email")

    return dumps(
        auth.auth_passwordreset_request(email)
    )

@APP.route('/auth/passwordreset/reset', methods=['POST'])
def auth_passwordreset_reset():
    """ Given a reset code, change user's password """

    reset_code = request.form.get("reset_code")
    new_password = request.form.get("new_password")

    return dumps(
        auth.auth_passwordreset_reset(reset_code, new_password)
    )

@APP.route('/channel/invite', methods=['POST'])
def channel_invite():
    """ Invite a user to join a channel """
    
    token = request.form.get("token")
    channel_id = request.form.get("channel_id")
    u_id = request.form.get("u_id")

    return dumps(
        channel.channel_invite(token, channel_id, u_id)
    )

@APP.route('/channel/details', methods=['GET'])
def channel_details():
    """ Provides basic details about a channel """
    
    token = request.args.get("token")
    channel_id = request.args.get("channel_id")

    return dumps(
        channel.channel_details(token, channel_id)
    )

@APP.route('/channel/messages', methods=['GET'])
def channel_messages():
    """ Returns up to 50 messages from a channel """

    token = request.args.get("token")
    channel_id = request.args.get("channel_id")
    start = request.args.get("start")

    return dumps(
        channel.channel_messages(token, channel_id, start)
    )

@APP.route('/channel/leave', methods=['POST'])
def channel_leave():
    """ Removes a user from a channel """
    
    token = request.form.get("token")
    channel_id = request.form.get("channel_id")

    return dumps(
        channel.channel_leave(token, channel_id)
    )

@APP.route('/channel/join', methods=['POST'])
def channel_join():
    """ Adds an authorised user to a channel """
    
    token = request.form.get("token")
    channel_id = request.form.get("channel_id")

    return dumps(
        channel.channel_join(token, channel_id)
    )

@APP.route('/channel/addowner', methods=['POST'])
def channel_addowner():
    """ Make a user an owner of the channel """
    
    token = request.form.get("token")
    channel_id = request.form.get("channel_id")
    u_id = request.form.get("u_id")

    return dumps(
        channel.channel_addowner(token, channel_id, u_id)
    )

@APP.route('/channel/removeowner', methods=['POST'])
def channel_removeowner():
    """ Removes a user as an owner of the channel """

    token = request.form.get("token")
    channel_id = request.form.get("channel_id")
    u_id = request.form.get("u_id")

    return dumps(
        channel.channel_removeowner(token, channel_id, u_id)
    )

@APP.route('/channel/list', methods=['GET'])
def channel_list():
    """ Provides a list of all channels that the user is a member of """
    
    token = request.args.get("token")

    return dumps(
        channel.channels_list(token)
    )

@APP.route('/channel/listall', methods=['GET'])
def channel_listall():
    """ Provides a list of all channel """

    token = request.args.get("token")

    return dumps(
        channel.channels_listall(token)
    )

@APP.route('/channel/create', methods=['POST'])
def channel_create():
    """ 
    Create a new channel with name that is either public or private
    """

    token = request.form.get("token")
    name = request.form.get("name")
    is_public = request.form.get("is_public")
    if is_public == "True":
        is_public_bool = True
    else:
        is_public_bool = False

    return dumps(
        channel.channels_create(token, name, is_public_bool)
    )

'''
MESSAGE
'''
@APP.route('/message/sendlater', methods=['POST'])
def message_sendlater():
    '''
    Sends a message from authorised_user to the channel specified by 
    channel_id automatically at a specified time in the future
    '''
    token = request.form.get("token")
    channel_id = request.form.get("channel_id")
    message = request.form.get("message")
    time_sent = request.form.get("time_sent")

    return dumps(
        message.message_sendlater(token, channel_id, message, time_sent)
    )


@APP.route('/message/send', methods=['POST'])
def message_send():
    '''
    Send a message from authorised_user to the channel specified by channel_id
    '''
    token = request.form.get("token")
    channel_id = request.form.get("channel_id")
    message = request.form.get("message")

    return dumps(
        message.message_send(token, channel_id, message)
    )

@APP.route('/message/remove', methods=['DELETE'])
def message_remove():
    '''
    Given a message_id for a message, this message is removed from the channel
    '''
    message_id = None 
    #TODO
    token = request.form.get("token")
    return dumps(
        message.message_remove(token, message_id)
    )

@APP.route('/message/edit', methods=['PUT'])
def message_edit():
    '''
    Given a message, update it's text with new text
    '''
    token = request.form.get("token")
    message_id = request.form.get("message_id")
    message = request.form.get("message")

    return dumps(
        message.message_edit(token, message_id, message)
    )

@APP.route('/message/react', methods=['POST'])
def message_react():
    '''
    Given a message within a channel the authorised user is part of,
     add a "react" to that particular message
    '''
    token = request.form.get("token")
    message_id = request.form.get("message_id")
    react_id = request.form.get("react_id")

    return dumps(
        message.message_react(token, message_id, react_id)
    )

@APP.route('/message/unreact', methods=['POST'])
def message_unreact():
    '''
    Given a message within a channel the authorised user is part of,
    remove a "react" to that particular message
    '''
    token = request.form.get("token")
    message_id = request.form.get("message_id")
    react_id = request.form.get("react_id")

    return dumps(
        message.message_unreact(token, message_id, react_id)
    )

@APP.route('/message/pin', methods=['POST'])
def message_pin():
    '''
    Given a message within a channel, mark it as "pinned" 
    '''
    token = request.form.get("token")
    message_id = request.form.get("message_id")

    return dumps(
        message.message_pin(token, message_id)
    )

@APP.route('/message/unpin', methods=['POST'])
def message_unpin():
    '''
    Given a message within a channel, remove its mark as "pinned" 
    '''
    token = request.form.get("token")
    message_id = request.form.get("message_id")

    return dumps(
        message.message_unpin(token, message_id)
    )



'''
USER 
'''

@APP.route('/user/profile', methods = ['GET'])
def user_profile():
    '''
    returns info about their email, first name, last name, handle
    '''
    token = request.args.get("token")
    u_id = request.args.get("u_id")

    return dumps(
        user.user_profile(token, u_id)
    )

@APP.route('/user/profile/setname', methods = ['PUT'])
def user_profile_setname():
    '''
    updates user's first and last name
    '''
    token = request.form.get("token")
    name_first = request.form.get("name_first")
    name_last = request.form.get("name_last")

    return dumps(
        user.user_profile_setname(token, name_first, name_last)
    )

@APP.route('/user/profile/setemail', methods = ['PUT'])
def user_profile_setemail():
    '''
    updates user's email
    '''
    token = request.form.get("token")
    email = request.form.get("email")

    return dumps(
        user.user_profile_setemail(token, email)
    )

@APP.route('/user/profile/sethandle', methods = ['PUT'])
def user_profile_setemail():
    '''
    updates user's handle(display name)
    '''
    token = request.form.get("token")
    handle_str = request.form.get("handle_str")

    return dumps(
        user.user_profile_sethandle(token, handle_str)
    )

@APP.route('/user/profiles/uploadphoto', methods = ['POST'])
def user_profiles_uploadphoto():
    '''
    Given a URL of an image on the internet, crops the image within x and 
    y coordinates

    '''
    token = request.form.get("token")
    img_url = request.form.get("img_url")
    x_start = request.form.get("x_start")
    y_start = request.form.get("y_start")
    x_end = request.form.get("x_end")
    y_end = request.form.get("y_end")

    return dumps(
        user.user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end)
    )

'''
STANDUP
'''

@APP.route('/standup/start', methods = ['POST'])
def standup_start():
    '''
    starts standup for 15 mins
    '''
    token = request.form.get("token")
    channel_id = request.form.get("channel_id")

    return dumps(
        standup.standup_start(token, channel_id)
    )

@APP.route('/standup/send', methods = ['POST'])
def standup_send():
    '''
    Sending a message to get buffered in the standup queue
    '''
    token = request.form.get("token")
    channel_id = request.form.get("channel_id")
    message = request.form.get("message")

    return dumps(
        standup.standup_send(token, channel_id, message)
    )

@APP.route('/search', methods = ['GET'])
def search():
    '''
    given a query, return matched messages in all of the channels that
    the user is part of
    '''
    token = request.args.get("token")
    query = request.args.get("query")
  
    return dumps(
        Search.search(token, query)
    )

@APP.route('/admin/userpermission/change', methods = ['POST'])
def admin_userpermission_change():
    '''
    Given a User by their user ID, set their permissions to new permissions
    described by permission_id
    '''
    token = request.form.get("token")
    u_id = request.form.get("u_id")
    permission_id = request.form.get("permission_id")
  
    return dumps(
        permission.admin_userpermission_change(token, u_id, permission_id)
    )



if __name__ == '__main__':
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))
