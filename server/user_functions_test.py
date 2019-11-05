'''
Testing user functions Iteration 2
Team: You_Things_Can_Choose
'''
import pytest
from server import user_functions as funcs
from server import auth_functions
import server.global_var as global_var
from server.Error import AccessError

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
              "name_last":'Smith', "handle_str":'raydonsmith'}

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
              "name_last":'World', "handle_str":'raydensmith'}


    # A name of 50 length is valid
    assert funcs.user_profile_setname(token, create_50_string(), \
         create_50_string()) == {}

    # First name too long
    with pytest.raises(ValueError, match="Name too long"):
        funcs.user_profile_setname(token, create_50_string() + "a", "Smith")

    # Lasts name too long
    with pytest.raises(ValueError, match="Name too long"):
        funcs.user_profile_setname(token, "Raydon", create_50_string() + "a")


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
              "name_last":'Smith', "handle_str":'raydensmith'}

    # A invalid email is given
    with pytest.raises(ValueError, match="Invalid email"):
        funcs.user_profile_setemail(token, "invalidEmail")

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
              "name_last":'Smith', "handle_str":'new handle'}


    # A invalid handle is given (50 characters)
    with pytest.raises(ValueError, match="Invalid Handle"):
        funcs.user_profile_sethandle(token, create_50_string())

    # A invalid handle is given (2 characters)
    with pytest.raises(ValueError, match="Invalid Handle"):
        funcs.user_profile_sethandle(token, "aa")


def test_profiles_uploadphoto():
    '''
    #Initialisation
    global_var.initialise_all()
    assert global_var.data["users"] == []

    #Creating a user
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
         "Rayden", "Smith")

    assert global_var.data["users"] != []
    token = user["token"]

    #A valid photo is uploaded and cropped
    assert funcs.user_profiles_uploadphoto(token, \
        "https://oc1.ocstatic.com/images/logo_small.png", 10, 10, 20 ,20) == {}

    #The url is invalid
    with pytest.raises(ValueError, match = "HTTP status not 200"):
        funcs.user_profiles_uploadphoto(token,\
            "https://oc1.ocstatic.com/images/logo_small.png1", 10, 10, 20, 20 )

    #Size of img2 = (0,0,256,256)
    with pytest.raises(ValueError, match = "Crop values invalid"):
        funcs.user_profiles_uploadphoto(token,\
            "https://oc1.ocstatic.com/images/logo_small.png", 0, 0, 200, 300)

'''

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
              "handle_str":'raydensmith'}]}

    # Creating a user
    user = auth_functions.auth_register("test2@gmail.com", "pass1234", \
         "Mary", "Lamb")

    assert funcs.users_all(token) == {"users":[
        {"u_id": 0, "email":'test@gmail.com', "name_first":'Rayden', \
             "name_last":'Smith', "handle_str":'raydensmith'},
        {"u_id": 1, "email":'test2@gmail.com', "name_first":'Mary', \
              "name_last":'Lamb', "handle_str":'marylamb'}]}

#Helper funcions

def create_50_string():
    '''
    Creates a string of length 50 characters
    '''
    string = "a" * 50
    assert len(string) == 50
    return string
