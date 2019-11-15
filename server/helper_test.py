'''
Functions to test helper
'''
import pytest
from server import auth_functions
import server.global_var as global_var
from server.Error import AccessError, ValueError
from server import helpers
from server import channel_functions
from server import message_functions

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
    assert encoded == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIj"\
    "p7InVfaWQiOiIxIn19.jFcUwcBtXw6pUWh8-K_cBgdYVouYebtuptYD55LEk4Y"

    encoded = helpers.encode_token_for_u_id({"u_id": "2521"})
    assert encoded == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIj"\
    "p7InVfaWQiOiIyNTIxIn19.AIupr3YzISaUBZq5b-osrslwhZyOaOlAEaMy0ECUWbc"

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

    with pytest.raises(AccessError, match="Invalid token"):
        helpers.token_is_admin("12345")

    token = user["token"]
    user = helpers.get_user_by_token(token)
    user.permission = 2
    assert helpers.token_is_admin(token) is True

    user.permission = 1
    assert helpers.token_is_admin(token) is False

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

    with pytest.raises(AccessError, match="Invalid token"):
        helpers.token_is_owner("12345")

    token = user["token"]
    user = helpers.get_user_by_token(token)
    user.permission = 1
    assert helpers.token_is_owner(token) is True
    user.permission = 0
    assert helpers.token_is_owner(token) is False

# Tests valid_email
def test_valid_email():
    """
    Ensures that valid_email returns
    """
    # Successful cases
    assert helpers.valid_email("email@gmail.com") is True
    assert helpers.valid_email("hello@gmail.com") is True
    assert helpers.valid_email("apple@g.com") is True
    assert helpers.valid_email("pineapple@hotmail.com.au") is True

    # Unsuccessful cases
    assert helpers.valid_email("apple") is False
    assert helpers.valid_email("apple@gma") is False
    assert helpers.valid_email("apple@.com") is False
    assert helpers.valid_email("@gmail.com") is False
    assert helpers.valid_email(".com.au") is False
    assert helpers.valid_email("apple.com") is False

# Checks if a name is valid
def test_valid_name():
    """
    Ensures that a user's name is valid
    """
    # Successful case
    assert helpers.valid_name("a") is True
    assert helpers.valid_name("a"*30) is True
    assert helpers.valid_name("a"*50) is True

    # Unsuccessful case
    assert helpers.valid_name("") is False
    assert helpers.valid_name("a"*51) is False
    assert helpers.valid_name("a"*212) is False

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

    assert helpers.valid_user_id(u_id) is True
    assert helpers.valid_user_id(-1) is False


# Changed valid_token to decorator. Not sure if it's possible to test like this
'''
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

    assert helpers.valid_token(token) is True
    assert helpers.valid_token("12345") is False

'''
# Testing possible permissions
def test_valid_permission_id():
    """
    Ensures that permission id is valid
    """
    # Testing owner
    assert helpers.valid_permission_id(1) is True

    # Testing admin
    assert helpers.valid_permission_id(2) is True

    # Testing user
    assert helpers.valid_permission_id(3) is True

    # Unsuccessful cases
    assert helpers.valid_permission_id(-5) is False
    assert helpers.valid_permission_id(0) is False
    assert helpers.valid_permission_id(4) is False
    assert helpers.valid_permission_id(522) is False

def test_get_user_by_u_id():
    """
    Ensures that get_user_by_u_id returns the correct u_id
    """
    # Initialisation
    global_var.initialise_all()
    assert global_var.data["users"] == []
    # Creating a user
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
         "Raydon", "Smith")
    u_id = user["u_id"]

    assert helpers.get_user_by_u_id(u_id).u_id == u_id

    with pytest.raises(ValueError, match="Invalid User ID"):
        helpers.get_user_by_u_id(-1)


def test_get_user_by_token():
    """
    Ensures that the correct user is obtained by get_user_by_token
    """
    # Initialisation
    global_var.initialise_all()
    assert global_var.data["users"] == []

    # Creating a user
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
        "Raydon", "Smith")
    u_id = user["u_id"]
    token = user["token"]

    assert (helpers.get_user_by_token(token)).u_id == u_id

    with pytest.raises(AccessError, match="Invalid token"):
        helpers.get_user_by_token("invalid_token")


def test_get_user_token_by_u_id():
    """
    Ensures that the correct token is obtained by get_user_token_by_u_id
    """
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
    """
    Ensures that get_user_by_reset_code obtains the correct user u_id
    """

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
    """
    Ensures the correct user is returned by email
    """
    # Initialisation
    global_var.initialise_all()

  	# Testing unsuccessful case
    assert None is helpers.get_user_by_email("2132@gmail.com")

  	# Testing successful case
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
        "Raydon", "Smith")
    u_id = user["u_id"]
    user_object = helpers.get_user_by_email("test@gmail.com")
    assert u_id == user_object.u_id

def test_remove_reset():
    """
    Ensures the reset is removed
    """
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
    assert success is True

def test_add_reset():
    """
    Ensures add_reset is only successful if code and u_id match
    """
    # Initialisation
    global_var.initialise_all()

    success = False
    helpers.add_reset("code1", 1)

    # Unsuccessful - Wrong reset code
    for reset_code in global_var.data["reset_code"]:
        if reset_code["reset_code"] == "invalid_reset_code" and \
        reset_code["user"] == 1:
            success = True
    assert success is False

    # Unsuccessful - Wrong user id
    for reset_code in global_var.data["reset_code"]:
        if reset_code["reset_code"] == "code1" and reset_code["user"] == -1:
            success = True
    assert success is False

    # Testing successful entry
    for reset_code in global_var.data["reset_code"]:
        if reset_code["reset_code"] == "code1" and reset_code["user"] == 1:
            success = True
    assert success is True

def test_get_channel_by_channel_id():
    # Initialisation
    global_var.initialise_all()

    # Creating a user
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
    "Raydon", "Smith")

    token = user["token"]
    # Creating channels
    # Creating first channel
    channel_1 = channel_functions.channels_create(token, "Channel 1", True)
    channel_1_id = channel_1["channel_id"]
    # Creating second channel
    channel_2 = channel_functions.channels_create(token, "Channel 2", True)
    channel_2_id = channel_2["channel_id"]
    # Ensuring that first channel has id
    assert helpers.get_channel_by_channel_id(channel_1_id).id == 0
    # Ensuring that second channel has id
    assert helpers.get_channel_by_channel_id(channel_2_id).id == 1

def test_get_channel_by_message_id():
    # Initalise
    global_var.initialise_all()
    # Creating a user
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
    "Raydon", "Smith")

    token = user["token"]
    # Create a channel
    channel = channel_functions.channels_create(token, "Channel 1", True)
    channel_id = channel["channel_id"]
    # Sending one message in channel
    assert message_functions.message_send(token, channel_id, "Hello Everyone") == {"message_id" : 0}
	# Check message obtain from first message
    assert helpers.get_channel_by_message_id(0).id == channel_id


def test_get_message_by_message_id():
	# Initalise
    global_var.initialise_all()

    # Creating a user
    user = auth_functions.auth_register("test@gmail.com", "pass123", \
    "Raydon", "Smith")
    token = user["token"]

    # Create channel
    channel = channel_functions.channels_create(token, "Channel 1", True)
    channel_id = channel["channel_id"]
    # Send message
    assert message_functions.message_send(token, channel_id, "Hello Everyone") == {"message_id" : 0}

    # Assert that channel id is the same as given by message
    assert helpers.get_message_by_message_id(0).message == "Hello Everyone"

def test_generate_handle():
    # Initialisation
    global_var.initialise_all()
    
    # First instance of handle in server
    user1 = auth_functions.auth_register("test1@gmail.com", "pass123", \
        "Ashley", "Huang")
    user1 = helpers.get_user_by_token(user1["token"])
    assert user1.handle == "ashleyhuang"
    
    # Non-first instance of handle in server - substitute found
    user2 = auth_functions.auth_register("test2@gmail.com", "pass123", \
    	"Ashley", "Huang")
    user2 = helpers.get_user_by_token(user2["token"])
    assert user2.handle == "1ashleyhuang"
    
    # Non-first instance of handle in server - first no substitute found
    auth_functions.auth_register("test3@gmail.com", "pass123", \
        "3Ashley", "Huang")
    user4 = auth_functions.auth_register("test4@gmail.com", "pass123", \
        "Ashley", "Huang")
    user4 = helpers.get_user_by_token(user4["token"])
    assert user4.handle == "0"

    # Non-first instance of handle in server - second no substitute found
    auth_functions.auth_register("test5@gmail.com", "pass123", \
        "5Ashley", "Huang")
    user6 = auth_functions.auth_register("test6@gmail.com", "pass123", \
        "Ashley", "Huang")
    user6 = helpers.get_user_by_token(user6["token"])
    assert user6.handle == "1"
    
def test_unique_handle():
    # Initialisation
    global_var.initialise_all()

    # Testing unique handle
    assert helpers.unique_handle("AshleyHuang") is True
    
    # Testing not unique handle
    user = auth_functions.auth_register("ashley@gmail.com", "pass123", \
        "Ashley", "Huang")

    assert helpers.unique_handle("ashleyhuang") is False
