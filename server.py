"""Flask server"""
from json import dumps
from flask import Flask, request

from global_var import data
from server.auth import auth_functions as auth

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



@APP.route('/auth/login', methods = ['POST'])
def auth_login():
    """ 
    Given a registered user' email and password, generates a valid token
    for the user to remain authenticated 
    """
    #Gets username and password
    email = request.form.get("email")
    password = request.form.get("password")

    #Calls function from auth_functions.py
    return auth.auth_login(email,password)

@APP.route('/auth/logout', methods = ['POST'])
def auth_logout():
    """ Description of function """
    return "You have reach auth_logout Endpoint"

@APP.route('/auth/register', methods = ['POST'])
def auth_register():
    """ 
    Given a user's details, creates a new account and returns a new token
    """
    #Gets user details
    email = request.form.get("email")
    password = request.form.get("password")
    name_first = request.form.get("name_first")
    name_last = request.form.get("name_last")

    return auth.auth_register(email,password,name_first,name_last)


@APP.route('/auth/passwordreset/request', methods = ['POST'])
def auth_passwordreset_request():
    """ Description of function """
    return "You have reach auth_passwordreset_request Endpoint"


@APP.route('/auth/passwordreset/reset', methods = ['POST'])
def auth_passwordreset_reset():
    """ Description of function """
    return "You have reach auth_passwordreset_reset Endpoint"


if __name__ == '__main__':
    APP.run()
