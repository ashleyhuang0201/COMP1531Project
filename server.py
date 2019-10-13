"""Flask server"""
from json import dumps
from flask import Flask, request

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
    """ Description of function """
    return "You have reach auth_login Endpoint"


@APP.route('/auth/logout', methods = ['POST'])
def auth_logout():
    """ Description of function """
    return "You have reach auth_logout Endpoint"


@APP.route('/auth/register', methods = ['POST'])
def auth_register():
    """ Description of function """
    return "You have reach auth_register Endpoint"


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
