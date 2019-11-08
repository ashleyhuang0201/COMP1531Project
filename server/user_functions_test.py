'''
Testing user functions Iteration 2
Team: You_Things_Can_Choose
'''
import pytest
from server import user_functions as funcs
from server import auth_functions
import server.global_var as global_var
from server.Error import AccessError
import urllib.request
from PIL import Image

def test_user_profile():
    '''
    Returns information about their email, first name, last name, and handle
    '''
    # Initialisation
    global_var.initialise_all()
    assert global_var.data["users"] == []

    # Creating a user
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
         "Raydon", "Smith")

    assert global_var.data["users"] != []

    token = user["token"]
    u_id = user["u_id"]

    # A valid user_id is provided, user details are returned
    assert funcs.user_profile(token, u_id) ==  \
         {"u_id": u_id, "email":'test@gmail.com', "name_first":'Raydon', \
              "name_last":'Smith', "handle_str":'raydonsmith', \
              "profile_img_url": None}

    # An exception occurs when the user_id is invalid
    with pytest.raises(ValueError, match="Invalid User ID"):
        funcs.user_profile(token, -1)

    # An exception occurs when token is invalid
    with pytest.raises(AccessError, match="Invalid token"):
        funcs.user_profile("invalid_token", u_id)

def test_profile_setname():
    '''
    Update the authorised user's first and last name
    '''
    # Initialisation
    global_var.initialise_all()
    assert global_var.data["users"] == []

    # Creating user
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
        "Rayden", "Smith")

    assert global_var.data["users"] != []

    token = user["token"]
    u_id = user["u_id"]

    # A valid first and last name is given
    assert funcs.user_profile_setname(token, "Rayden", "Smith") == {}

    # Updating the first and last name of user
    funcs.user_profile_setname(token, "Hello", "World")

    # Checking if first and last name have been updated successfully
    assert funcs.user_profile(token, u_id) ==  \
         {"u_id": u_id, "email":'test@gmail.com', "name_first":'Hello', \
              "name_last":'World', "handle_str":'raydensmith', \
              "profile_img_url": None}


    # A name of 50 length is valid
    assert funcs.user_profile_setname(token, create_50_string(), \
         create_50_string()) == {}

    # First name too long
    with pytest.raises(ValueError, match="Name too long"):
        funcs.user_profile_setname(token, create_50_string() + "a", "Smith")

    # Lasts name too long
    with pytest.raises(ValueError, match="Name too long"):
        funcs.user_profile_setname(token, "Raydon", create_50_string() + "a")

    # An exception occurs when token is invalid
    with pytest.raises(AccessError, match="Invalid token"):
        funcs.user_profile_setname("invalid_token", "Raydon", "Smith")


def test_profile_setemail():
    '''
    Update the user's email
    '''
    # Initialisation

    global_var.initialise_all()
    assert global_var.data["users"] == []

    # Creating user
    user = auth_functions.auth_register("test@gmail.com", "pass123",\
        "Rayden", "Smith")

    assert global_var.data["users"] != []

    token = user["token"]
    u_id = user["u_id"]

    # An email already in use is given
    with pytest.raises(ValueError, match="Email already in use"):
        funcs.user_profile_setemail(token, "test@gmail.com")

    # A valid email change
    assert funcs.user_profile_setemail(token, "test1@gmail.com") == {}

    # Updating the email of the user
    funcs.user_profile_setemail(token, "new@gmail.com")

    # Checking if the user's email has been updated successfully
    assert funcs.user_profile(token, u_id) ==  \
         {"u_id": u_id, "email":'new@gmail.com', "name_first":'Rayden', \
              "name_last":'Smith', "handle_str":'raydensmith', \
              "profile_img_url": None}

    # A invalid email is given
    with pytest.raises(ValueError, match="Invalid email"):
        funcs.user_profile_setemail(token, "invalidEmail")

    # An exception occurs when token is invalid
    with pytest.raises(AccessError, match="Invalid token"):
        funcs.user_profile_setemail("invalid_token", "test1234@gmail.com")

def test_profile_sethandle():
    '''
    Update the user's handle
    '''
    # Initialisation
    global_var.initialise_all()
    assert global_var.data["users"] == []

    # Creating a user
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
         "Rayden", "Smith")

    assert global_var.data["users"] != []

    token = user["token"]
    u_id = user["u_id"]

    # A valid handle is given
    assert funcs.user_profile_sethandle(token, "a handle") == {}

    # Updating the handle of the user
    funcs.user_profile_sethandle(token, "new handle")

    # Checking if the user's handle has been updated successfully
    assert funcs.user_profile(token, u_id) ==  \
         {"u_id": u_id, "email":'test@gmail.com', "name_first":'Rayden', \
              "name_last":'Smith', "handle_str":'new handle', \
              "profile_img_url": None}


    # A invalid handle is given (50 characters)
    with pytest.raises(ValueError, match="Invalid Handle"):
        funcs.user_profile_sethandle(token, create_50_string())

    # A invalid handle is given (2 characters)
    with pytest.raises(ValueError, match="Invalid Handle"):
        funcs.user_profile_sethandle(token, "aa")

    # An exception occurs when token is invalid
    with pytest.raises(AccessError, match="Invalid token"):
        funcs.user_profile_sethandle("invalid_token", "helloworld")


def test_profiles_uploadphoto():

    #Initialisation
    global_var.initialise_all()
    assert global_var.data["users"] == []

    #Creating a user
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
         "Rayden", "Smith")

    assert global_var.data["users"] != []
    token = user["token"]

    #750 x 738 dimension
    #Testing photo url
    test_url = "https://i.redd.it/51p5c1efueoy.jpg"

    #A valid photo is uploaded and cropped
    assert funcs.user_profiles_uploadphoto(token, test_url, 0, 0, 20 ,20) == {}

    #The test_url is invalid
    with pytest.raises(ValueError, match = "HTTP status not 200"):
        funcs.user_profiles_uploadphoto(token, \
        "https://invalid_url.jpg", 10, 10, 20, 20 )

    #Size of img = (0,0,750,738)
    with pytest.raises(ValueError, match = "x_start is invalid"):
        funcs.user_profiles_uploadphoto(token, test_url, -1, 0, 700, 700)

    with pytest.raises(ValueError, match = "x_start is invalid"):
        funcs.user_profiles_uploadphoto(token, test_url, 760, 0, 700, 700)

    with pytest.raises(ValueError, match = "x_end is invalid"):
        funcs.user_profiles_uploadphoto(token, test_url, 0, 0, -1, 700)

    with pytest.raises(ValueError, match = "x_end is invalid"):
        funcs.user_profiles_uploadphoto(token, test_url, 0, 0, 800, 700)

    with pytest.raises(ValueError, match = "y_start is invalid"):
        funcs.user_profiles_uploadphoto(token, test_url, 0, -1, 700, 700)

    with pytest.raises(ValueError, match = "y_start is invalid"):
        funcs.user_profiles_uploadphoto(token, test_url, 0, 800, 700, 700)

    with pytest.raises(ValueError, match = "y_end is invalid"):
        funcs.user_profiles_uploadphoto(token, test_url, 0, 0, 700, -1)

    with pytest.raises(ValueError, match = "y_end is invalid"):
        funcs.user_profiles_uploadphoto(token, test_url, 0, 0, 700, 800)

    #if x_start == x_end
    with pytest.raises(ValueError, match = \
    "An image of no pixels is not an image"):
        funcs.user_profiles_uploadphoto(token, test_url, 10, 0, 10, 700)

    #if y_start == y_end
    with pytest.raises(ValueError, match = \
    "An image of no pixels is not an image"):
        funcs.user_profiles_uploadphoto(token, test_url, 0, 10, 700, 10)

    with pytest.raises(ValueError, match = "Image uploaded is not a JPG"):
        funcs.user_profiles_uploadphoto(token, \
        "https://myrealdomain.com/images/corgi-dogs-pictures-7.png", \
        0, 10, 200, 700)

    # An exception occurs when token is invalid
    with pytest.raises(AccessError, match="Invalid token"):
        funcs.user_profiles_uploadphoto("invalid_tok", test_url, 10, 10, 20, 20)


def test_users_all():
    '''
    Shows all users
    '''
    # Initialisation
    global_var.initialise_all()
    assert global_var.data["users"] == []

    # Creating a user
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
         "Rayden", "Smith")

    assert global_var.data["users"] != []

    token = user["token"]

    assert funcs.users_all(token) == {"users":[{"u_id": 0, \
         "email":'test@gmail.com', "name_first":'Rayden', "name_last":'Smith', \
              "handle_str":'raydensmith', "profile_img_url": None}]}

    # Creating a user
    user = auth_functions.auth_register("test2@gmail.com", "pass1234", \
         "Mary", "Lamb")

    assert funcs.users_all(token) == {"users":[
        {"u_id": 0, "email":'test@gmail.com', "name_first":'Rayden', \
             "name_last":'Smith', "handle_str":'raydensmith', \
             "profile_img_url": None},
        {"u_id": 1, "email":'test2@gmail.com', "name_first":'Mary', \
              "name_last":'Lamb', "handle_str":'marylamb', \
              "profile_img_url": None}]}

    # An exception occurs when token is invalid
    with pytest.raises(AccessError, match="Invalid token"):
        funcs.users_all("invalid_token")

#Helper funcions

def create_50_string():
    '''
    Creates a string of length 50 characters
    '''
    string = "a" * 50
    assert len(string) == 50
    return string
