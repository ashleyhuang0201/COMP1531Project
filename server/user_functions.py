#Dummy implementations of functions user_*
#Created by: Michael Zhang
#Created on: 1/10/2019

import pytest

"""
For a valid user, returns information about their email, first name, last name, and handle

ValueError:
- User with u_id is not a valid user
"""
def user_profile(token, u_id):
    email = "test@gmail.com"
    name_first = "Raydon"
    name_last = "Smith"
    handle_str = "raydonsmith"
    return email, name_first, name_last, handle_str

"""
Update the authorised user's first and last name

ValueError:
- name_first is more than 50 characters
- name_last is more than 50 characters
"""
def user_profile_setname(token, name_first, name_last):
    pass

"""
Updates the authorised user's email address

ValueError:
- Email entered is not a valid email
- Email address is already being used by another user

"""
def user_profile_setemail(token, email):
    pass

"""
Update the authorised user's handle

ValueError:
- handle_str is more than 20 characters
"""
def user_profile_sethandle(token, handle_str):
    pass

"""
Given a URL of an image on the internet, crops the image within x and y co-oridinates

ValueError:
- img_url returns an HTTP status other than 200
- xy points are outside the dimensions of the image at the url

"""
def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    pass