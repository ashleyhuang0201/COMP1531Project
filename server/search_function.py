# Dummy implementation of search() fucntion
# Created by: Coen Townson
# Created on: 2/10/2019

import pytest
from server.search import search_function_test as test

matches = []

# Dummy search function and returns
def search(token, query_str):
    if (query_str == '93336257 Multichannel search '):
        # Messages 'Multichannel search 2' and 'Multichannel search 1' respectively
        # Ordered this way since I'm assuming search should return most recent 
        # results first
        matches.append(test.messages2[0])
        matches.append(test.messages1[0])
    elif (query_str == '93336255 Singlechannel match '):
        # Messages 'Singlechannel search 2' and 'Singlechannel search 1' respectively
        matches.append(test.messages1[2])
        matches.append(test.messages1[3])
    elif (query_str == '93336256 Only this'):
        # Message 'Only this'
        matches.append(test.messages1[1])

    return {'messages': matches}