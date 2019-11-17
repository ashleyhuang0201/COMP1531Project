'''
Functions to test helper
'''
import pytest
from server import auth_functions as auth
import server.global_var as global_var
from server import (channel_functions, helpers,
                    message_functions)
from server.Error import AccessError, ValueError

# Tests decode_token
def test_decode_token():
    '''
    Decode token
    '''

    # Initialisation
    global_var.initialise_all()

    encoded = helpers.encode_token_for_u_id({"u_id": "1"})
    assert {"u_id": "1"} == helpers.decode_token(encoded)

    encoded = helpers.encode_token_for_u_id({"u_id": "2521"})
    assert {"u_id": "2521"} == helpers.decode_token(encoded)

# Test encode token for u_id
def test_encode_token_for_u_id():
    '''
    Encode
    '''
    # Initialisation
    global_var.initialise_all()

    encoded = helpers.encode_token_for_u_id({"u_id": "1"})
    assert encoded == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIj"\
    "p7InVfaWQiOiIxIn19.jFcUwcBtXw6pUWh8-K_cBgdYVouYebtuptYD55LEk4Y"

    encoded = helpers.encode_token_for_u_id({"u_id": "2521"})
    assert encoded == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIj"\
    "p7InVfaWQiOiIyNTIxIn19.AIupr3YzISaUBZq5b-osrslwhZyOaOlAEaMy0ECUWbc"

def test_activate_token():
    '''
    Tests activate token
    '''
    # Initialisation
    global_var.initialise_all()

    # Successfully adding token
    helpers.activate_token("token")
    assert global_var.data["tokens"][0] == "token"

def test_deactive_token():
    '''
    Tests a token as inactive
    '''

    # Initialisation
    global_var.initialise_all()

    # Adding token
    helpers.activate_token("token")

    # Removing token
    assert helpers.deactive_token("token") is True
    assert len(global_var.data["tokens"]) == 0

    # Removing token which doesn't exist
    assert helpers.deactive_token("token") is False

def test_get_new_u_id():
    '''
    Returns a new u_id
    '''

    # Initialisation
    global_var.initialise_all()

    # Creating a user
    auth.auth_register("test@gmail.com", "pass123", "Raydon", "Smith")

    assert helpers.get_new_u_id() == 1

    # Creating a user
    auth.auth_register("test12@gmail.com", "pass1234", "Kevin", "Zhu")

    assert helpers.get_new_u_id() == 2

def test_add_user():
    '''
    Appends a new user object to the data
    '''

    # Initialisation
    global_var.initialise_all()

    # Adding user
    helpers.add_user("user")

    assert global_var.data["users"][0] == "user"

# Test token is admin
def test_token_is_admin():
    '''
    Tests for if a token is related to an admin
    '''
	# Initialisation
    global_var.initialise_all()

    # Creating a user
    user = auth.auth_register("test@gmail.com", "pass123", "Raydon", "Smith")

    with pytest.raises(AccessError, match="Invalid Token"):
        helpers.token_is_admin("12345")

    token = user["token"]
    user = helpers.get_user_by_token(token)
    user.permission = 2
    assert helpers.token_is_admin(token) is True

    user.permission = 1
    assert helpers.token_is_admin(token) is False

# Test for token is owner
def test_token_is_owner():
    '''
    Test if a token is in an owner
    '''

	# Initialisation
    global_var.initialise_all()

    # Creating a user
    user = auth.auth_register("test@gmail.com", "pass123", "Raydon", "Smith")

    with pytest.raises(AccessError, match="Invalid Token"):
        helpers.token_is_owner("-1")

    token = user["token"]
    user = helpers.get_user_by_token(token)
    user.permission = 1
    assert helpers.token_is_owner(token) is True
    user.permission = 0
    assert helpers.token_is_owner(token) is False

# Tests valid_email
def test_valid_email():
    '''
    Ensures that valid_email returns
    '''
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
    '''
    Ensures that a user's name is valid
    '''
    # Successful case - name within range
    assert helpers.valid_name("a") is True
    assert helpers.valid_name("a" * 30) is True
    assert helpers.valid_name("a" * 50) is True

    # No name
    assert helpers.valid_name("") is False

    # Name too long
    assert helpers.valid_name("a" * 51) is False
    assert helpers.valid_name("a" * 212) is False


# Checks if a token is valid
def test_valid_token():
    '''
    Ensures that a user's token is valid
    '''
    # Defining test function
    @helpers.valid_token
    def function(token):
        return token

    # Invalid token
    with pytest.raises(AccessError, match="Invalid token"):
        function("-1")

    # Valid token
    user = auth.auth_register("ashley@gmail.com", "secure_password", \
        "Ashley", "Huang")
    assert function(user["token"]) == user["token"]

# Testing possible permissions
def test_valid_permission_id():
    '''
    Ensures that permission id is valid
    '''
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
    '''
    Ensures that get_user_by_u_id returns the correct u_id
    '''
    # Initialisation
    global_var.initialise_all()

    # Creating a user
    user = auth.auth_register("test@gmail.com", "pass123", "Raydon", "Smith")
    u_id = user["u_id"]

    assert helpers.get_user_by_u_id(u_id).u_id == u_id

    with pytest.raises(ValueError, match="Invalid User ID"):
        helpers.get_user_by_u_id(-1)

def test_get_user_by_token():
    '''
    Ensures that the correct user is obtained by get_user_by_token
    '''

    # Initialisation
    global_var.initialise_all()

    # Creating a user
    user = auth.auth_register("test@gmail.com", "pass123", "Raydon", "Smith")
    u_id = user["u_id"]
    token = user["token"]

    assert helpers.get_user_by_token(token).u_id == u_id

    with pytest.raises(AccessError, match="Invalid Token"):
        helpers.get_user_by_token("invalid_token")

def test_get_user_token_by_u_id():
    '''
    Ensures that the correct token is obtained by get_user_token_by_u_id
    '''

    # Initialisation
    global_var.initialise_all()

    # Creating a user
    user = auth.auth_register("test@gmail.com", "pass123", "Raydon", "Smith")

    assert helpers.get_user_token_by_u_id(user["u_id"]) == user["token"]

    with pytest.raises(AccessError, match="Invalid Token"):
        helpers.get_user_by_token(-1)

def test_get_user_by_reset_code():
    '''
    Ensures that get_user_by_reset_code obtains the correct user u_id
    '''

    # Initialisation
    global_var.initialise_all()

    # Creating a user
    user = auth.auth_register("test@gmail.com", "pass123", "Raydon", "Smith")
    u_id = user["u_id"]

    auth.auth_passwordreset_request("test@gmail.com")
    reset_code = auth.generate_reset_code(u_id)

    assert helpers.get_user_by_reset_code(reset_code) == u_id

    assert helpers.get_user_by_reset_code(-1) is None

def test_get_user_by_email():
    '''
    Ensures the correct user is returned by email
    '''

    # Initialisation
    global_var.initialise_all()

  	# Testing unsuccessful case
    assert helpers.get_user_by_email("2132@gmail.com") is None

  	# Testing successful case
    user = auth.auth_register("test@gmail.com", "pass123", "Raydon", "Smith")
    u_id = user["u_id"]
    user_object = helpers.get_user_by_email("test@gmail.com")

    assert u_id == user_object.u_id

def test_remove_reset():
    '''
    Ensures the reset is removed
    '''

    # Initialisation
    global_var.initialise_all()

    # Unsuccessful case
    with pytest.raises(ValueError, match="No code was deleted"):
        helpers.remove_reset("code1")

    # Successful case
    helpers.add_reset("code1", 1)
    helpers.remove_reset("code1")
    for reset_code in global_var.data["reset_code"]:
        if reset_code["reset_code"] == "code1":
            raise ValueError("Remove reset code unsuccessful")

def test_add_reset():
    '''
    Ensures add_reset is only successful if code and u_id match
    '''

    # Initialisation
    global_var.initialise_all()

    helpers.add_reset("code1", 1)

    # Unsuccessful - Wrong reset code
    for reset_code in global_var.data["reset_code"]:
        if reset_code["reset_code"] == "invalid_reset_code" and \
        reset_code["user"] == 1:
            raise ValueError("Wrong reset code")

    # Unsuccessful - Wrong user id
    for reset_code in global_var.data["reset_code"]:
        if reset_code["reset_code"] == "code1" and reset_code["user"] == -1:
            raise ValueError("Wrong user id")

    # Testing successful entry
    success = False
    for reset_code in global_var.data["reset_code"]:
        if reset_code["reset_code"] == "code1" and reset_code["user"] == 1:
            success = True
    assert success is True

def test_get_channel_by_channel_id():
    '''
    Ensures get_channel_by_channel_id returns correct channel id
    '''

    # Initialisation
    global_var.initialise_all()

    # Creating a user
    user = auth.auth_register("test@gmail.com", "pass123", "Raydon", "Smith")
    token = user["token"]

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

    # Checking no such channel_id
    assert helpers.get_channel_by_channel_id(-1) is None

def test_get_channel_by_message_id():
    '''
    Ensures get_channel_by_message_id returns the correct channel
    '''
    # Initalise
    global_var.initialise_all()
    # Creating a user
    user = auth.auth_register("test@gmail.com", "pass123", "Raydon", "Smith")

    token = user["token"]
    # Create a channel
    channel = channel_functions.channels_create(token, "Channel 1", True)
    channel_id = channel["channel_id"]
    # Sending one message in channel
    assert message_functions.message_send(token, channel_id, "Hello Everyone")\
        == {"message_id" : 0}
	# Check message obtain from first message
    assert helpers.get_channel_by_message_id(0).id == channel_id

    # Checking no such message_id
    assert helpers.get_channel_by_message_id(-1) is None

def test_get_message_by_message_id():
    '''
    Ensures get_message_by_message_id returns the correct message
    '''
	# Initalise
    global_var.initialise_all()

    # Creating a user
    user = auth.auth_register("test@gmail.com", "pass123", "Raydon", "Smith")
    token = user["token"]

    # Create channel
    channel = channel_functions.channels_create(token, "Channel 1", True)
    channel_id = channel["channel_id"]
    # Send message
    assert message_functions.message_send(token, channel_id, "Hello Everyone")\
        == {"message_id" : 0}

    # Assert that channel id is the same as given by message
    assert helpers.get_message_by_message_id(0).message == "Hello Everyone"

    # Checking no such message_id
    assert helpers.get_message_by_message_id(-1) is None

def test_generate_handle():
    '''
    Ensures handles that are generated are unique
    '''
    # Initialisation
    global_var.initialise_all()

    # First instance of handle in server
    user1 = auth.auth_register("test1@gmail.com", "pass123", "Ashley", "Huang")
    user1 = helpers.get_user_by_token(user1["token"])
    assert user1.handle == "ashleyhuang"

    # Non-first instance of handle in server - substitute found
    user2 = auth.auth_register("test2@gmail.com", "pass123", "Ashley", "Huang")
    user2 = helpers.get_user_by_token(user2["token"])
    assert user2.handle == "1ashleyhuang"

    # Non-first instance of handle in server - first no substitute found
    auth.auth_register("test3@gmail.com", "pass123", "3Ashley", "Huang")
    user4 = auth.auth_register("test4@gmail.com", "pass123", "Ashley", "Huang")
    user4 = helpers.get_user_by_token(user4["token"])
    assert user4.handle == "0"

    # Non-first instance of handle in server - second no substitute found
    auth.auth_register("test5@gmail.com", "pass123", "5Ashley", "Huang")
    user6 = auth.auth_register("test6@gmail.com", "pass123", "Ashley", "Huang")
    user6 = helpers.get_user_by_token(user6["token"])
    assert user6.handle == "1"

def test_unique_handle():
    '''
    Ensure that handles are unique
    '''
    # Initialisation
    global_var.initialise_all()

    # Testing unique handle
    assert helpers.unique_handle("AshleyHuang") is True

    # Testing not unique handle
    user = auth.auth_register("ashley@gmail.com", "pass123", "Ashley", "Huang")
    get_user = helpers.get_user_by_token(user["token"])
    assert helpers.unique_handle(get_user.handle) is False

def test_valid_crop():
    '''
    Ensure given values for cropping are valid
    '''
    # Initialisation
    global_var.initialise_all()

    # Test errors
    # x_start is before the first pixel
    with pytest.raises(ValueError, match="x_start is invalid"):
        helpers.valid_crop(-2, 2, 2, 4, 100, 100)

    # x_start is on the last pixel
    with pytest.raises(ValueError, match="x_start is invalid"):
        helpers.valid_crop(100, 100, 2, 20, 100, 400)

    # x_start is after the last pixel
    with pytest.raises(ValueError, match="x_start is invalid"):
        helpers.valid_crop(200, 100, 2, 40, 100, 600)

    # x_end is before the first pixel
    with pytest.raises(ValueError, match="x_end is invalid"):
        helpers.valid_crop(20, -1, 10, 20, 100, 40)

    # x_end is after the last pixel
    with pytest.raises(ValueError, match="x_end is invalid"):
        helpers.valid_crop(2, 20, 2, 10, 10, 20)

    # x_end is the first pixel
    with pytest.raises(ValueError, match="x_end is invalid"):
        helpers.valid_crop(0, 0, 2, 10, 20, 20)

    # y_start is before the first pixel
    with pytest.raises(ValueError, match="y_start is invalid"):
        helpers.valid_crop(2, 10, -1, 10, 20, 20)

    # y_start is on the last pixel
    with pytest.raises(ValueError, match="y_start is invalid"):
        helpers.valid_crop(2, 10, 40, 10, 20, 40)

    # y_start is after the last pixel
    with pytest.raises(ValueError, match="y_start is invalid"):
        helpers.valid_crop(2, 10, 400, 20, 50, 50)

    # y_end is the first pixel
    with pytest.raises(ValueError, match="y_end is invalid"):
        helpers.valid_crop(2, 10, 0, 0, 20, 20)

    # y_end is after the last pixel
    with pytest.raises(ValueError, match="y_end is invalid"):
        helpers.valid_crop(2, 10, 20, 400, 20, 50)

    # y_end is before the first pixel
    with pytest.raises(ValueError, match="y_end is invalid"):
        helpers.valid_crop(2, 10, 1, -1, 50, 50)

    # x_start == x_end
    with pytest.raises(ValueError, match=\
        "An image of no pixels is not an image"):
        helpers.valid_crop(2, 2, 5, 10, 20, 20)

    # y_start == y_end
    with pytest.raises(ValueError, match=\
        "An image of no pixels is not an image"):
        helpers.valid_crop(2, 10, 5, 5, 20, 20)

    # Successful crop
    assert helpers.valid_crop(2, 4, 1, 4, 100, 100) is True

def test_get_reset_code_from_email():
    ''' Returns a reset_code according to a user email '''

    # Register a user
    user = auth.auth_register("registered@g.com", "passsword", "a", "b")
    user = helpers.get_user_by_token(user["token"])

    # No such email request
    assert helpers.get_reset_code_from_email("-1@gmail.com") is None

    # Reset email request
    auth.auth_passwordreset_request(user.email)
    assert helpers.get_reset_code_from_email(user.email) ==\
        global_var.data["reset_code"][0]["reset_code"]

def test_to_int():
    ''' Typecasting to int '''

    with pytest.raises(ValueError, match=\
        "Value was missing - please check you input"):
        helpers.to_int(None)

    with pytest.raises(ValueError, match="Value entered was not of type int"):
        helpers.to_int("a")

    with pytest.raises(ValueError, match="Value entered was not of type int"):
        helpers.to_int("5a")

    assert helpers.to_int(3.5) == 3
    assert helpers.to_int(3.521) == 3
    assert helpers.to_int(False) == 0
    assert helpers.to_int(True) == 1
    assert helpers.to_int(5) == 5
    assert helpers.to_int("5") == 5

def test_to_bool():
    ''' Typecasting to bool '''

    with pytest.raises(ValueError, match=\
        "Value was missing - please check you input"):
        helpers.to_bool(None)

    assert helpers.to_bool(True) is True
    assert helpers.to_bool(False) is False
    assert helpers.to_bool(True) == 1
    assert helpers.to_bool("1") == 1
    assert helpers.to_bool(1) is True
    assert helpers.to_bool("") is False

def test_to_float():
    ''' Typecasting to float '''

    with pytest.raises(ValueError, match=\
        "Value was missing - please check you input"):
        helpers.to_float(None)

    with pytest.raises(ValueError, match="Value entered was not of type float"):
        helpers.to_float("a")

    assert helpers.to_float(5) == 5
    assert helpers.to_float(True) == 1
    assert helpers.to_float(False) == 0
    assert helpers.to_float(3.521) == 3.521
    assert helpers.to_float("5.231123123") == 5.231123123
