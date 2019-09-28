import re # Used to validate email (validEmail)

# Given functions
# Given a registered users' email and password and generates a valid token for the user to remain authenticated
def auth_login(email, password):
    if validUser(email) == True and validEmail(email) == True and validPassword(password) == True:
        # Login success
        return "123456"
    else:
        # Login failure
        return "404"

# Helper Functions
# Checks if an email is a valid email
def validEmail(email):  
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if re.search(regex, email):
        return True
    else:
        return False

# Checks if a password is a valid password
# Password must have at least 5 characters
def validPassword(password):
    if len(password) >= 5:
        return True
    else:
        return False

# Checks if a user is a valid user
def validUser(email):
    if email == "test@gmail.com":
        # Valid user
        return True
    else:
        # Invalid user
        return False