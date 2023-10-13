import flask
import time
import hashlib
import secrets

import app.models as models
import app.dbh.dbhelper as dbhelper

TOKEN_EXPIRY = 30 * 24 * 3600 # 30 days

def user_from_request(request: flask.Request) -> models.user.User:
    """Gets the authenticated user from the request's cookies containing the api token
    returns None if token is invalid or no token is in cookies"""
    
    key = request.cookies.get("api_key")
    print(request.cookies.keys())

    if key is None:
        return None

    token = dbhelper.get(models.token.Token, models.token.Token.token, key)
    if token is None or token.expiry < time.time():
        return None
    else:
        return token.user

def validate_login(username: str, password: str) -> bool:
    result = dbhelper.get(models.user.User, models.user.User.name, username)

    if result is None:
        return False

    hash = hashlib.sha256(password.encode("utf8") + result.password_salt).digest()
    return hash == result.password_hash

def create_token(user: models.user.User) -> models.token.Token:
    token_unique = False
    token_token = ""
    while not token_unique:
        token_token = secrets.token_hex(models.token.TOKEN_LENGTH // 2)
        if not validate_token(token_token):
            token_unique = True

    # delete the old token in case it exists
    try:
        dbhelper.delete_expression(models.token.Token, models.token.Token.token == token)
    except:
        pass

    token = models.token.Token()
    token.token = token_token
    token.expiry = int(time.time()) + TOKEN_EXPIRY
    token.username = user.name

    dbhelper.create(token)

    return token

def validate_token(token: str) -> bool:
    # only return true if the token exists and is still valid
    result = dbhelper.get(models.token.Token, models.token.Token.token, token)

    return False if result is None else time.time() > result.expiry
    