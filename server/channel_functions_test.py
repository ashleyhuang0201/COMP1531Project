#Testing for channel_functions
#Created by Ashley Huang
#Created on 2/10/2019

import pytest
import channel_functions as func

def test_channel_invite():
    assert func.channel_invite(token, channel, id) == {}

def test_channel_details():
    assert func.channel_details(token, channel) == {name, owner_members, all_members}

def test_channel_messages():
    assert func.channel_messages(token, channel, start) == {messages, start, end}

def test_channel_leave():
    assert func.channel_leave(token, channel) == {}

def test_channel_join():
    assert func.channel_join(token, channel) == {}

def test_channel_addowner():
    assert func.channel_addowner(token, channel, id) == {}

def test_channel_removeowner():
    assert func.channel_removeowner(token, channel, id) == {}

def test_channels_list():
    assert func.channels_list(token) == {channels}

def test_channels_listall():
    assert func.channels_listall(token) == {channels}

def test_channels_create():
    assert func.channels_create(token, name, is_public) == {channel}
