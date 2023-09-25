import flask
import time

import app.models as models
import app.dbh.dbhelper as dbhelper

def user_from_request(request: flask.Request) -> models.user.User:
    """Gets the authenticated user from the request's cookies containing the api token
    returns None if token is invalid or no token is in cookies"""
    
    key = request.cookies.get("api_key")

    if key is None:
        return None

    token = dbhelper.get_token(key)
    if token.expiry < time.time():
        return None
    else:
        return token.user