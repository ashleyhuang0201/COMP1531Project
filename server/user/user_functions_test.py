#Functions for testing user_* functions
#Created by: Michael Zhang
#Created on: 1/10/2019

import pytest
from . import user_functions as funcs
from server.auth import auth_functions
from server.helper.Error import AccessError


def test_user_profile():
    
    #Initialisation
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
         "Rayden", "Smith")
    token = user["token"]
    u_id = user["u_id"]

    #A valid user_id is provided, user details are returned
    assert funcs.user_profile(token, u_id) ==  \
         {"email":'test@gmail.com', "name_first":'Raydon',"name_last":'Smith', \
              "handle_str":'raydonsmith'}

    #A exception occurs when the user_id is invalid
    with pytest.raises(ValueError, match = "Invalid User ID"):
        funcs.user_profile(token, 99)


def test_profile_setname():
    
    #Initialisation
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
         "Rayden", "Smith")
    token = user["token"]

    #A valid first and last name is given
    assert funcs.user_profile_setname(token, "Raydon", "Smith") == {}

    #A name of 50 length is valid
    assert funcs.user_profile_setname(token, create_50_string(), \
         create_50_string()) == {}

    #First name too long
    with pytest.raises(ValueError, match = "Name too long"):
        funcs.user_profile_setname(token, create_50_string() + "a", "Smith" )

    #Lasts name too long
    with pytest.raises(ValueError, match = "Name too long"):
        funcs.user_profile_setname(token, "Raydon", create_50_string() + "a")

      
def test_profile_setemail():
   
    #Initialisation
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
         "Rayden", "Smith")

    user2 = auth_functions.auth_register("test2@gmail.com", "pass123", \
         "Bob", "Sally")
    token = user["token"]

    #A valid email change
    assert funcs.user_profile_setemail(token, "test1@gmail.com") == {}

    #A invalid email is given
    with pytest.raises(ValueError, match = "Invalid email"):
        funcs.user_profile_setemail(token, "invalidEmail")

    #A email already in use is given
    with pytest.raises(ValueError, match = "Email already in use"):
        funcs.user_profile_setemail(token, "test2@gmail.com")


def test_profile_sethandle():
    
    #Initialisation
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
         "Rayden", "Smith")
    token = user["token"]

    #A valid handle is given
    assert funcs.user_profile_sethandle(token, "a handle") == {}

    #A invalid handle is given
    with pytest.raises(ValueError, match = "Invalid Handle"):
        funcs.user_profile_sethandle(token, create_50_string())


def test_profiles_uploadphoto():
    
    #Initialisation
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
         "Rayden", "Smith")
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



#Helper funcions

#Creates a string of length 50 characters
def create_50_string():
    string = ""
    for i in range(50):
        string += "a"

    assert len(string) == 50
    return string