import server.global_var as global_var
from server.helpers import valid_token

def search(token, query_str):
    """
    Given a query string, return a collection of messages in all of the
    channels that the user has joined that match the query
    """
    # Checking if the token is a valid token
    if not valid_token(token):
        raise ValueError("Invalid token")

    # Searching for messages with query string
    messages = []
    for channel in global_var.data["channels"]:
        if channel.user_in_channel(token):
            messages = messages + channel.search_message(query_str)
    
    return {"messages": messages}