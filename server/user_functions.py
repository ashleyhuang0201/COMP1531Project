'''
User functions Iteration 2 implementations
Team: You_Things_Can_Choose
'''
from server.Error import AccessError
from server.helpers import get_user_by_u_id, get_user_by_token,\
valid_user_id, valid_email, valid_token, get_user_by_email
import server.global_var as global_var

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

    #ADD PROFILE_IMG_URL
    user_profile_return = {"u_id": u_id, "email": user.email, \
         "name_first": user.name_first, "name_last": user.name_last, \
              "handle_str": user.handle}

    return user_profile_return

def user_profile_setname(token, name_first, name_last):
    """
    Update the authorised user's first and last name

    ValueError:
    - name_first is more than 50 characters
    - name_last is more than 50 characters
    """
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

    if len(handle_str) > 20 or len(handle_str) < 3:
        raise ValueError("Invalid Handle")

    # Changes user's handle in database

    user = get_user_by_token(token)

    # Update user's handle
    user.update_handle(handle_str)

    return {}
'''
def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    
    Given a URL of an image on the internet, crops the image within x and
    y co-oridinates

    ValueError:
    - img_url returns an HTTP status other than 200 (2xx indicates success)
    - xy points are outside the dimensions of the image at the url


    # This function is a little hard to test, as we don't know how the image
    # are to be handled

    valid_urls = {"img1", "img2"}

    if img_url in valid_urls:
        pass
    else:
        raise ValueError("HTTP status not 200")

    # Check that the crop co-ordinates are valid

    pass
    
    if valid_crop(x_start, y_start, x_end, y_end) == False:
        raise ValueError("Crop values invalid")

    
    # The user's profile picture is changed
    return {}
'''

def users_all(token):
    '''
    Shows all users
    '''
    all_users = []

    for user in global_var.data["users"]:

        #ADD PROFILE_IMG_URL
        user_profile_return = {"u_id": user.u_id, "email": user.email, \
         "name_first": user.name_first, "name_last": user.name_last, \
              "handle_str": user.handle}
        all_users.append(user_profile_return)

    return {"users": all_users}
