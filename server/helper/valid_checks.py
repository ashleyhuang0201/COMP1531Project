import re

# Checks if an email is a valid email
def valid_email(email):
	if re.search('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', email):
		return True
	else: 
		return False

# Checks if a user_id is valid
def valid_user_id(u_id):
    if u_id  == "valid_u_id":
        return True
    return False

# Checks if a user_id is valid
def valid_token(token):
    if token  == "valid_token":
        return True
    return False