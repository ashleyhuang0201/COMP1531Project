'''
Team: You_Things_Can_Choose
Tests echo
'''

import server.echo as echo

def test_echo():
    '''
    Tests echo: Single character, multiple characters
    '''
    assert echo.echo("1") == "1", "1 == 1"
    assert echo.echo("abc") == "abc", "abc == abc"
    assert echo.echo("trump") == "trump", "trump == trump"
