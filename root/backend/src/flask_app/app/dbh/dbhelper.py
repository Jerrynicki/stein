import sqlalchemy
from app.extensions import db
import app.models as models

import secrets
import time
import hashlib

TOKEN_EXPIRY = 30 * 24 * 3600 # 30 days

def create_user(user: models.user.User):
    db.session.add(user)
    db.session.flush()
    db.session.commit()

def get_user(username: str):
    result = db.session.execute(
        sqlalchemy.select(
            models.user.User
        ).where(
            models.user.User.name == username
        )
    ).scalar_one_or_none()
    return result


def validate_login(username: str, password: str) -> bool:
    result = db.session.execute(
        sqlalchemy.select(
            models.user.User
        ).where(
            models.user.User.name == username
        )
    ).scalar_one_or_none()

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
        db.session.execute(
            sqlalchemy.delete(
                models.token.Token
            ).where(
                models.token.Token.token == token
            )
        )
    except:
        pass

    token = models.token.Token()
    token.token = token_token
    token.expiry = int(time.time()) + TOKEN_EXPIRY
    token.username = user.name

    db.session.add(token)

    db.session.flush()
    db.session.commit()

    return token

def validate_token(token: str) -> bool:
    # only return true if the token exists and is still valid
    result = get_token(token)

    return False if result is None else time.time() > result.expiry
    
def get_token(token: str) -> models.token.Token:
    result = db.session.execute(
        sqlalchemy.select(
            models.token.Token
        ).where(
            models.token.Token.token == token 
        )
    ).scalar_one_or_none()

    return result

def get_teams() -> list[models.team.Team]:
    # TODO
    a = models.team.Team()
    a.color = "#FFFFFF"
    a.name = "Stein"
    a.id = 1
    return [a]

def create_post(post: models.post.Post) -> int:
    """Returns the generated post id"""

    db.session.add(post)
    db.session.flush()
    db.session.commit()

    return post.id

def get_post(id: int) -> models.post.Post:
    result = db.session.execute(
        sqlalchemy.select(
            models.post.Post
        ).where(
            models.post.Post.id == id 
        )
    ).scalar_one_or_none()

    return result