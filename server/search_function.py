"""
Search functions
search: Search for a message using a substring
"""
import server.global_var as global_var
from server.helpers import valid_token, get_user_by_token

@valid_token
def search(token, query_str):
    """
    Given a query string, return a collection of messages in all of the
    channels that the user has joined that match the query
    """

    # Searching for messages with query string
    messages = []
    for channel in global_var.data["channels"]:
        if channel.user_in_channel(get_user_by_token(token).u_id):
            messages = messages + channel.search_message(token, query_str)

    return {"messages": messages}
