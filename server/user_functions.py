'''
User functions Iteration 2 implementations
Team: You_Things_Can_Choose
'''

import urllib
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from PIL import Image
from flask import request

from server.Error import ValueError
import server.global_var as global_var
from server.helpers import get_user_by_u_id, get_user_by_token, valid_user_id,\
    valid_email, valid_token, get_user_by_email, valid_crop, unique_handle, \
    create_photo_path
from server.constants import MAX_NAME_LENGTH, MAX_HANDLE_LENGTH, \
    MIN_HANDLE_LENGTH

@valid_token
def user_profile(token, u_id):
    """
    For a valid user, returns information about their email, first name,
    last name, and handle

    ValueError:
    - User with u_id is not a valid user
    """

    if valid_user_id(u_id) is False:
        raise ValueError("Invalid User ID")

    # Get user object by u_id
    user = get_user_by_u_id(u_id)

    user_profile_return = {
        "u_id": user.u_id,
        "email": user.email,
        "name_first": user.name_first,
        "name_last": user.name_last,
        "handle_str": user.handle,
        "profile_img_url": user.has_photo
    }

    return user_profile_return

@valid_token
def user_profile_setname(token, name_first, name_last):
    """
    Update the authorised user's first and last name

    ValueError:
    - name_first is more than 50 characters
    - name_last is more than 50 characters
    """

    if len(name_first) > MAX_NAME_LENGTH:
        raise ValueError("Name too long")
    if len(name_last) > MAX_NAME_LENGTH:
        raise ValueError("Name too long")

    user = get_user_by_token(token)

    # Update user's first name
    user.update_name_first(name_first)

    # Update user's last name
    user.update_name_last(name_last)

    return {}

@valid_token
def user_profile_setemail(token, email):
    """
    Updates the authorised user's email address

    ValueError:
    - Email entered is not a valid email
    - Email address is already being used by another user

    """

    user = get_user_by_email(email)
    if valid_email(email) is False:
        raise ValueError("Invalid email")
    if user:
        raise ValueError("Email already in use")

    # Changes user's email in database
    user = get_user_by_token(token)

    # Update user's email
    user.update_email(email)

    return {}

@valid_token
def user_profile_sethandle(token, handle_str):
    """
    Update the authorised user's handle
    """
    if len(handle_str) > MAX_HANDLE_LENGTH or len(handle_str) < MIN_HANDLE_LENGTH:
        raise ValueError("Invalid Handle")
    if not unique_handle(handle_str):
        raise ValueError("Handle Taken")

    # Changes user's handle in database
    user = get_user_by_token(token)

    # Update user's handle
    user.update_handle(handle_str)

    return {}

@valid_token
def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    """
    Given a URL of an image on the internet, crops the image within x and
    y co-oridinates

    ValueError:
    - img_url returns an HTTP status other than 200 (2xx indicates success)
    - xy points are outside the dimensions of the image at the url
    """

    req = Request(img_url, headers={"User-Agent": "Mozilla/5.0"})
    # Checking if the img_url is an accessable URL
    try:
        response = urlopen(req)
    except HTTPError as e:
        print(e)
        raise ValueError(f"The server cannot fulfil the request: {e.code}")
    except URLError as e:
        raise ValueError(f"The server cannot be reached: {e.reason}")

    # Obtaining image
    image_object = Image.open(response)

    # Checks if image is a jpg
    if image_object.format != "JPEG":
        raise ValueError("Image uploaded is not a JPG")

    # Check that the crop co-ordinates are valid
    # Getting the width and height of image
    width, height = image_object.size

    # Checking if the crop coordinates are within the bounds of the image
    valid_crop(x_start, x_end, y_start, y_end, width, height)

    # Obtaining user_id (user_id will be the unique filename)
    user = get_user_by_token(token)

    img_file_path = f"server/assets/images/{create_photo_path(user)}.jpg"


    # Gets image from url and saves it in images folder
    urllib.request.urlretrieve(img_url, img_file_path)

    # Cropping image
    img_file = open(img_file_path, "wb")
    cropped = image_object.crop((x_start, y_start, x_end, y_end))
    cropped.save(img_file)

    # Use request in running server context and give default url for unit tests
    try:
        url = request.host_url
    except:
        url = "http://localhost:5001/"
    user.upload_photo(f"{url}imgurl/{img_file_path}")

    return {}

@valid_token
def users_all(token):
    '''
    Shows all users
    '''

    all_users = []

    for user in global_var.data["users"]:
        user_profile_return = {
            "u_id": user.u_id,
            "email": user.email,
            "name_first": user.name_first,
            "name_last": user.name_last,
            "handle_str": user.handle,
            "profile_img_url":user.has_photo
        }
        all_users.append(user_profile_return)

    return {"users": all_users}
