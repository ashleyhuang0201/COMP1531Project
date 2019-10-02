# Dummy implementation of search() fucntion
# Created by: Coen Townson
# Created on: 2/10/2019

import pytest
import search_function_test as test
import channel_functions as channel

matches = [];

# Dummy search function and returns
def search(token, query_str):
    if (query_str == 'Multichannel'):
        # Messages 'Multichannel search 2' and 'Multichannel search 1' respectively
        # Ordered this way since I'm assuming search should return most recent 
        # results first
        matches.append(test.messages2[0])
        matches.append(test.messages1[0])
        return matches
    elif (query_str == 'Singlechannel'):
        # Messages 'Singlechannel search 2' and 'Singlechannel search 1' respectively
        matches.append(test.messages1[2])
        matches.append(test.messages1[3])
        return matches
    elif (query_str == 'Only'):
        # Message 'Only this'
        matches.append(test.messages1[1])
        return matches
    else:
        return [[]]