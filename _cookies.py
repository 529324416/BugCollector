import flask


COOKIE_DURATION = 24*3600*30

class CookieKeys:
    '''Cookie keys for the website.'''

    THEME = "theme"

def cookies(default_theme="dark"):
    '''get all the current cookies'''

    _cookies = {}
    for key in flask.request.cookies:
        _cookies[key] = flask.request.cookies.get(key, default_theme)
    return _cookies

class CookieHelper:

    def __init__(self, head=None):
        '''Initialize the CookieHelper.'''

        self.__head = head

    def _key(self, key):
        '''Get the value of a cookie.'''

        if self.__head == None:
            return key
        return f'{self.__head}_{key}'
    
    def get_cookie(self, key, default=None):
        '''Get the value of a cookie.'''

        return flask.request.cookies.get(self._key(key), default)

    def set_cookie_to(self, key, value, response) -> flask.Response:
        '''Set the value of a cookie to a response.'''

        response.set_cookie(self._key(key), value, max_age=COOKIE_DURATION)
        return response