#Functions for testing user_* functions
#Created by: Michael Zhang
#Created on: 1/10/2019

import pytest
import user_functions as funcs


def test_user_profile():
    
    #A valid user_id is provided, user details are returned
    assert funcs.user_profile("123456", 1) == ("test@gmail.com", "Raydon", "Smith", "raydonsmith")

    #A exception occurs when the user_id is invalid
    with pytest.raises(ValueError, match = "Invalid User ID"):
        funcs.user_profile("123456", 99)


def test_profile_setname():
    
    #A valid first and last name is given
    funcs.user_profile_setname("123456", "Raydon", "Smith")

    #A name of 50 length is valid
    funcs.user_profile_setname("123456", create_50_string(), create_50_string())

    #First name too long
    with pytest.raises(ValueError, match = "Name too long"):
        funcs.user_profile_setname("123456", create_50_string() + "a", "Smith" )

    #Lasts name too long
    with pytest.raises(ValueError, match = "Name too long"):
        funcs.user_profile_setname("123456", "Raydon", create_50_string() + "a")

      
def test_profile_setemail():
   
    #A valid email change
    funcs.user_profile_setemail("123456", "test1@gmail.com")

    #A invalid email is given
    with pytest.raises(ValueError, match = "Invalid email"):
        funcs.user_profile_setemail("123456", "invalidEmail")

    #A email already in use is given
    with pytest.raises(ValueError, match = "Email already in use"):
        funcs.user_profile_setemail("123456", "test2@gmail.com")


def test_profile_sethandle():
    
    #A valid handle is given
    funcs.user_profile_sethandle("123456", "a handle")

    #A invalid handle is given
    with pytest.raises(ValueError, match = "Invalid Handle"):
        funcs.user_profile_sethandle("123456", create_50_string())


def test_profiles_uploadphoto():
    
    #A valid photo is uploaded and cropped
    funcs.user_profiles_uploadphoto("123456", "img1", 10, 10, 20 ,20)

    #The url is invalid
    with pytest.raises(ValueError, match = "HTTP status not 200"):
        funcs.user_profiles_uploadphoto("123456","img3", 10, 10, 20, 20 )

    with pytest.raises(ValueError, match = "Crop bounds invalid"):
        funcs.user_profiles_uploadphoto("123456", "img1", -10,-10,50,50)

    with pytest.raises(ValueError, match = "Crop bounds invalid"):
        funcs.user_profiles_uploadphoto("123456", "img1", 0,0,110,50)

    with pytest.raises(ValueError, match = "Crop bounds invalid"):
        funcs.user_profiles_uploadphoto("123456", "img2", 10,10,20,60)


def create_50_string():
    string = ""
    for i in range(50):
        string += "a"

    assert len(string) == 50
    return string
