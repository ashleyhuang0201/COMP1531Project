'''
User functions Iteration 2 implementations
Team: You_Things_Can_Choose
'''
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import urllib
from PIL import Image
from server.Error import AccessError
import server.global_var as global_var
from server.helpers import get_user_by_u_id, get_user_by_token, valid_user_id,\
valid_email, valid_token, get_user_by_email, valid_crop

def user_profile(token, u_id):
    """
    For a valid user, returns information about their email, first name,
    last name, and handle

    ValueError:
    - User with u_id is not a valid user
    """

    if valid_user_id(u_id) is False:
        raise ValueError("Invalid User ID")

    if valid_token(token) is False:
        raise AccessError("Invalid token")


    # Get user object by u_id
    user = get_user_by_u_id(u_id)

    user_profile_return = {"u_id": u_id, "email": user.email, \
         "name_first": user.name_first, "name_last": user.name_last, \
              "handle_str": user.handle, "profile_img_url": \
              user.photo}

    return user_profile_return

def user_profile_setname(token, name_first, name_last):
    """
    Update the authorised user's first and last name

    ValueError:
    - name_first is more than 50 characters
    - name_last is more than 50 characters
    """
    if valid_token(token) is False:
        raise AccessError("Invalid token")
    if len(name_first) > 50:
        raise ValueError("Name too long")
    if len(name_last) > 50:
        raise ValueError("Name too long")

    user = get_user_by_token(token)

    # Update user's first name
    user.update_name_first(name_first)

    # Update user's last name
    user.update_name_last(name_last)

    return {}

def user_profile_setemail(token, email):
    """
    Updates the authorised user's email address

    ValueError:
    - Email entered is not a valid email
    - Email address is already being used by another user

    """
    if valid_token(token) is False:
        raise AccessError("Invalid token")

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

def user_profile_sethandle(token, handle_str):

    """
    Update the authorised user's handle

    ValueError:
    - handle_str is more than 20 characters
    """
    if valid_token(token) is False:
        raise AccessError("Invalid token")

    if len(handle_str) > 20 or len(handle_str) < 3:
        raise ValueError("Invalid Handle")

    # Changes user's handle in database

    user = get_user_by_token(token)

    # Update user's handle
    user.update_handle(handle_str)

    return {}

def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    """
    Given a URL of an image on the internet, crops the image within x and
    y co-oridinates

    ValueError:
    - img_url returns an HTTP status other than 200 (2xx indicates success)
    - xy points are outside the dimensions of the image at the url
    """
    # Checking if the user token is valid
    if valid_token(token) is False:
        raise AccessError("Invalid token")

    # Checking if the img_url is an accessable URL
    try:
        response = urlopen(img_url)
    except HTTPError as e:
        raise ValueError(f"The server cannot fulfil the request: {e.code}")
    except URLError as e:
        raise ValueError(f"The server cannot be reached: {e.reason}")

    # Obtaining image
    imageObject = Image.open(response)

    # Checks if image is a jpg
    if imageObject.format != "JPEG":
        raise ValueError("Image uploaded is not a JPG")

    # Check that the crop co-ordinates are valid
    # Getting the width and height of image
    width, height = imageObject.size

    # Checking if the crop coordinates are within the bounds of the image
    valid_crop(x_start, x_end, y_start, y_end, width, height)


    # Obtaining user_id (user_id will be the unique filename)
    user = get_user_by_token(token)
    u_id = user.u_id

    # Gets image from url and saves it in images folder
    urllib.request.urlretrieve(img_url, "../assets/images/user_profile/" + str(u_id) + ".jpg")

    # Cropping image
    cropped = imageObject.crop((x_start, y_start, x_end, y_end))
    cropped.save("../assets/images/user_profile/" + str(u_id) + ".jpg")

    user.upload_photo()

    return {}

def users_all(token):
    '''
    Shows all users
    '''
    if valid_token(token) is False:
        raise AccessError("Invalid token")

    all_users = []

    for user in global_var.data["users"]:
        user_profile_return = {"u_id": user.u_id, "email": user.email, \
         "name_first": user.name_first, "name_last": user.name_last, \
              "handle_str": user.handle, "profile_img_url": \
              user.photo}
        all_users.append(user_profile_return)

    return {"users": all_users}
