import flask

_available_themes = ["dark", "pastel", "wireframe"]

def fetch_theme(default="dark"):
    '''Fetch the theme from the cookie.'''

    theme = flask.request.cookies.get("theme")
    if theme == None:return default
    return theme

def set_theme(theme):
    '''Set the theme of the website.'''

    if theme not in _available_themes:
        return flask.make_response(f"invalid theme: {theme}", 404)
    response = flask.make_response("Theme set to " + theme, 200)
    _duration = 24*3600*30
    response.set_cookie("theme", theme, max_age=_duration, samesite=None)
    return response