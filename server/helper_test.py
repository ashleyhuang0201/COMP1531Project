'''
Functions to test helper
'''
import pytest
from server import user_functions
from server import auth_functions
import server.global_var as global_var
from server.Error import AccessError
from server import helpers

# Tests decode_token
def test_decode_token():
    """
    Decode token
    """
    # Initialisation
    global_var.initialise_all()

    encoded = helpers.encode_token_for_u_id({"u_id": "1"})
    assert {"u_id": "1"} == helpers.decode_token(encoded)

    encoded = helpers.encode_token_for_u_id({"u_id": "2521"})
    assert {"u_id": "2521"} == helpers.decode_token(encoded)

# Test encode token for u_id
def test_encode_token_for_u_id():
    """
    Encode
    """
    # Initialisation
    global_var.initialise_all()
    
    encoded = helpers.encode_token_for_u_id({"u_id": "1"})
    assert encoded == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjp7InVfaWQiOiIxIn19.jFcUwcBtXw6pUWh8-K_cBgdYVouYebtuptYD55LEk4Y"

    encoded = helpers.encode_token_for_u_id({"u_id": "2521"})
    assert encoded == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjp7InVfaWQiOiIyNTIxIn19.AIupr3YzISaUBZq5b-osrslwhZyOaOlAEaMy0ECUWbc"

# Test token is admin
def test_token_is_admin():
    """
    Tests for if a token is related to an admin
    """
	# Initialisation
    global_var.initialise_all()

    # Creating a user
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
         "Raydon", "Smith")
    
    with pytest.raises(ValueError, match="Invalid token"):
        helpers.token_is_admin("12345")
    
    token = user["token"]
    user = helpers.get_user_by_token(token)
    user.permission = 2
    assert helpers.token_is_admin(token) == True

    user.permission = 1
    assert helpers.token_is_admin(token) == False

# Test for token is owner
def test_token_is_owner():
    """
    Test if a token is in an owner
    """
  
	# Initialisation
    global_var.initialise_all()
    assert global_var.data["users"] == []
    # Creating a user
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
         "Raydon", "Smith")
    
    with pytest.raises(ValueError, match="Invalid token"):
        helpers.token_is_owner("12345")
    
    token = user["token"]
    user = helpers.get_user_by_token(token)
    user.permission = 1
    assert helpers.token_is_owner(token) == True
    user.permission = 0
    assert helpers.token_is_owner(token) == False
  
# Tests valid_email
def test_valid_email():
    """
    Ensures that valid_email returns
    """
    # Successful cases
    assert helpers.valid_email("email@gmail.com") == True
    assert helpers.valid_email("hello@gmail.com") == True
    assert helpers.valid_email("apple@g.com") == True
    assert helpers.valid_email("pineapple@hotmail.com.au") == True

    # Unsuccessful cases
    assert helpers.valid_email("apple") == False
    assert helpers.valid_email("apple@gma") == False
    assert helpers.valid_email("apple@.com") == False
    assert helpers.valid_email("@gmail.com") == False
    assert helpers.valid_email(".com.au") == False
    assert helpers.valid_email("apple.com") == False

# Checks if a name is valid
def test_valid_name():
    """
    Ensures that a user's name is valid
    """
    # Successful case
    assert helpers.valid_name("a") == True
    assert helpers.valid_name("a"*30) == True
    assert helpers.valid_name("a"*50) == True

    # Unsuccessful case
    assert helpers.valid_name("") == False
    assert helpers.valid_name("a"*51) == False
    assert helpers.valid_name("a"*212) == False

# Tests valid_user_id
def test_valid_user_id():
    """
    Ensures that a user's u_id is valid when in data
    and not valid when not in data
    """
    # Initialisation
    global_var.initialise_all()
    assert global_var.data["users"] == []
    # Creating a user
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
         "Raydon", "Smith")
    u_id = user["u_id"]
    
    assert helpers.valid_user_id(u_id) == True
    assert helpers.valid_user_id(-1) == False
    

# Checks if a token is valid
def test_valid_token():
    """
    Ensures that a user's token is valid
    """

    # Initialisation
    global_var.initialise_all()
    assert global_var.data["users"] == []
    # Creating a user
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
            "Raydon", "Smith")
    token = user["token"]

    assert helpers.valid_token(token) == True
    assert helpers.valid_token("12345") == False

# Testing possible permissions
def test_valid_permission_id():
    # Testing owner
    assert helpers.valid_permission_id(1) == True

    # Testing admin
    assert helpers.valid_permission_id(2) == True

    # Testing user
    assert helpers.valid_permission_id(3) == True

    # Unsuccessful cases
    assert helpers.valid_permission_id(-5) == False
    assert helpers.valid_permission_id(0) == False
    assert helpers.valid_permission_id(4) == False
    assert helpers.valid_permission_id(522) == False
    
def test_get_user_by_u_id():
    
    # Initialisation
    global_var.initialise_all()
    assert global_var.data["users"] == []
    # Creating a user
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
         "Raydon", "Smith")
    u_id = user["u_id"]
    
    assert helpers.get_user_by_u_id(u_id).u_id == u_id
    
    with pytest.raises(ValueError, match= "Invalid User ID"):
    	helpers.get_user_by_u_id(-1)
  
  
def test_get_user_by_token():
    # Initialisation
    global_var.initialise_all()
    assert global_var.data["users"] == []

    # Creating a user
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
        "Raydon", "Smith")
    u_id = user["u_id"]
    token = user["token"]

    assert (helpers.get_user_by_token(token)).u_id == u_id

    with pytest.raises(AccessError, match= "Invalid token"):
        helpers.get_user_by_token("invalid_token")


def test_get_user_token_by_u_id():
    # Initialisation
    global_var.initialise_all()
    assert global_var.data["users"] == []
    # Creating a user
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
            "Raydon", "Smith")
    token = user["token"]
    u_id = user["u_id"]

    assert helpers.get_user_token_by_u_id(u_id) == token

    with pytest.raises(AccessError, match="Invalid token"):
        helpers.get_user_by_token(-1)


def test_get_user_by_reset_code():

    # Initialisation
    global_var.initialise_all()

    assert global_var.data["users"] == []

    # Creating a user
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
            "Raydon", "Smith")
    u_id = user["u_id"]

    auth_functions.auth_passwordreset_request("test@gmail.com")
    reset_code = auth_functions.generate_reset_code(u_id)

    assert u_id == helpers.get_user_by_reset_code(reset_code)

def test_get_user_by_email():
    # Initialisation
    global_var.initialise_all()

  	# Testing unsuccessful case
    assert None == helpers.get_user_by_email("2132@gmail.com")
  
  	# Testing successful case
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
        "Raydon", "Smith")
    u_id = user["u_id"]
    user_object = helpers.get_user_by_email("test@gmail.com")
    assert u_id == user_object.u_id

def test_remove_reset():
    # Initialisation
    global_var.initialise_all()

	# Unsuccessful case
    with pytest.raises(ValueError, match="No code was deleted"):
    	helpers.remove_reset("code1")

	# Successful case
    helpers.add_reset("code1", 1)
    helpers.remove_reset("code1")
    success = True
    for reset_code in global_var.data["reset_code"]:
      	if reset_code["reset_code"] == "code1":
          	success = False
    assert success == True

def test_add_reset():
    # Initialisation
    global_var.initialise_all()

    success = False
    helpers.add_reset("code1", 1)

    # Unsuccessful - Wrong reset code
    for reset_code in global_var.data["reset_code"]:
      	if reset_code["reset_code"] == "invalid_reset_code" and reset_code["user"] == 1:
          	success = True
    assert success == False

    # Unsuccessful - Wrong user id
    for reset_code in global_var.data["reset_code"]:
      	if reset_code["reset_code"] == "code1" and reset_code["user"] == -1:
          	success = True
    assert success == False
    
    # Testing successful entry
    for reset_code in global_var.data["reset_code"]:
      	if reset_code["reset_code"] == "code1" and reset_code["user"] == 1:
          	success = True
    assert success == True

