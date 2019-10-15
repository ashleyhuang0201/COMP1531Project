# Checks if a user is an admin
def token_is_admin(token):
    if token  == "admin_token":
        return True
    return False

# Checks if a user is an owner
def token_is_owner(token):
    if token  == "owner_token":
        return True
    return False