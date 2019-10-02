# Dummy implementation of search() fucntion
# Created by: Coen Townson
# Created on: 2/10/2019

import pytest
import datetime


m1 = {'u_id' : 1, 'message' : 'First message', 'time_created' : datetime.datetime.now(), 'is_unread' : True}
m2 = {'u_id' : 2, 'message' : 'Not First message', 'time_created' : datetime.datetime.now(), 'is_unread' : False}
m3 = {'u_id' : 3, 'message' : 'Third message', 'time_created' : datetime.datetime.now(), 'is_unread' : True}

# Dummy search function and returns
def search(token, query_str):
    if (query_str == 'message'):
        return [[m1, m2, m3]]
    elif (query_str == 'First'):
        return [[m1, m2]]
    elif (query_str == 'Third'):
        return [[m3]]
    else:
        return [[]]