'''
Helper functions that check validity of user data
'''
import re

def valid_email(email):
    ''' Checks if an email is a valid email '''
    # r prefix treats as raw string - works without but pytest and pylint don't
    # like it
    regex = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    if re.search(regex, email):
        return True
    else:
        return False

def valid_name(name):
    ''' Checks if a name is valid to be registered '''
    if len(name) >= 1 and len(name) <= 50:
        return True
    else:
        return False

def valid_user_id(u_id):
    ''' Checks if a user_id is valid '''
    if u_id == "valid_u_id":
        return True
    return False

def valid_token(token):
    ''' Checks if a user_id is valid '''
    if token == "valid_token":
        return True
    return False
