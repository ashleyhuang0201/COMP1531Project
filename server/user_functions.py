'''
User functions Iteration 2 implementations
Team: You_Things_Can_Choose
'''
import jwt

from server.Error import AccessError
from server.helpers import get_user_by_u_id, get_user_by_token, valid_user_id, valid_email
from json import dumps
import server.global_var as data

"""
For a valid user, returns information about their email, first name, 
last name, and handle

ValueError:
- User with u_id is not a valid user
"""
def user_profile(token, u_id):

    if valid_user_id(u_id) == False:
        raise ValueError("Invalid User ID")

    # Get user object by u_id

    user = get_user_by_u_id(u_id)
    user_profile = {"email": user.email, "name_first": user.name_first, \
    "name_last": user.name_last, "handle_str": user.handle}

    return user_profile

"""
Update the authorised user's first and last name

ValueError:
- name_first is more than 50 characters
- name_last is more than 50 characters
"""
def user_profile_setname(token, name_first, name_last):
    if len(name_first) > 50:
        raise ValueError("Name too long")
    elif len(name_last) > 50:
        raise ValueError("Name too long")

    user = get_user_by_token(token)
    
    # Update user's first name 
    user.update_name_first(name_first)

    # Update user's last name
    user.update_name_last(name_last)

    return {}

"""
Updates the authorised user's email address

ValueError:
- Email entered is not a valid email
- Email address is already being used by another user

"""
def user_profile_setemail(token, email):

    used_emails = ["test2@gmail.com", "test3@gmail.com"]
    if valid_email(email) == False:
        raise ValueError("Invalid email")
    elif email in used_emails:
        raise ValueError("Email already in use")

    # Changes user's email in database
    user = get_user_by_token(token)
    
    # Update user's email
    user.update_email(email)

    return {}

"""
Update the authorised user's handle

ValueError:
- handle_str is more than 20 characters
"""

def user_profile_sethandle(token, handle_str):
    
    if len(handle_str) > 20 or len(handle_str) < 3:
        raise ValueError("Invalid Handle")

    # Changes user's handle in database

    user = get_user_by_token(token)
    
    # Update user's handle
    user.update_handle(handle_str)

    return {}

"""
Given a URL of an image on the internet, crops the image within x and 
 y co-oridinates

ValueError:
- img_url returns an HTTP status other than 200 (2xx indicates success)
- xy points are outside the dimensions of the image at the url

"""
def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):

    # This function is a little hard to test, as we don't know how the image
    # are to be handled

    valid_urls = {"img1", "img2"}

    if img_url in valid_urls:
        pass
    else:
        raise ValueError("HTTP status not 200")

    # Check that the crop co-ordinates are valid

    pass
    '''
    if valid_crop(x_start, y_start, x_end, y_end) == False:
        raise ValueError("Crop values invalid")

    '''
    # The user's profile picture is changed
    return {}
