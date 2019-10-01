#Dummy implementations of functions user_*
#Created by: Michael Zhang
#Created on: 1/10/2019

import pytest
import re

"""
For a valid user, returns information about their email, first name, last name, and handle

ValueError:
- User with u_id is not a valid user
"""
def user_profile(token, u_id):

    if valid_user_id(u_id) == False:
        raise ValueError("Invalid User ID")

    #Dummy user profile returned
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
    if len(name_first) > 50:
        raise ValueError("Name too long")
    elif len(name_last) > 50:
        raise ValueError("Name too long")

    #Changes user's name in database

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

    #Changes user's email in database


"""
Update the authorised user's handle

ValueError:
- handle_str is more than 20 characters
"""
def user_profile_sethandle(token, handle_str):
    if len(handle_str) > 20:
        raise ValueError("Invalid Handle")

    #Changes user's handle in database

"""
Given a URL of an image on the internet, crops the image within x and y co-oridinates

ValueError:
- img_url returns an HTTP status other than 200 (2xx indicates success)
- xy points are outside the dimensions of the image at the url

"""
def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    #This function is a little hard to test, as we haven't implemented the url 
    #dummy urls, where the tuple is x_start, y_start, x_end, y_end
    urls = {"img1": (0,0,100,100), "img2":(0,0,50,50)}

    if img_url in urls:
        pass
    else:
        raise ValueError("HTTP status not 200")
    
    if urls[img_url][0] > x_start:
        raise ValueError("Crop bounds invalid")
    elif urls[img_url][1] > y_start:
        raise ValueError("Crop bounds invalid")
    elif urls[img_url][2] < x_end:
        raise ValueError("Crop bounds invalid")
    elif urls[img_url][3] < y_end:
        raise ValueError("Crop bounds invalid")
    #The user's profile picture is changed


# Checks if an email is a valid email
def valid_email(email):  
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if re.search(regex, email):
        return True
    else:
        return False

def valid_user_id(user_id):
    if user_id == 1:
        return True
    return False