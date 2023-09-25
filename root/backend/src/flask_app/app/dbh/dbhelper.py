import sqlalchemy
from app.extensions import db
import app.models as models

def create_user(user: models.user.User):
    db.session.add(user)
    db.session.flush()
    db.session.commit()

def get_user(username: str):
    result = db.session.execute(
        sqlalchemy.select(
            models.user.User
        ).where(
            models.user.User.username == username
        )
    ).scalar_one_or_none()
    return result


def validate_login(username: str, password: str) -> bool:
    pass

def create_token(user: models.user.User) -> models.token.Token:
    pass

def validate_token(token: str) -> bool:
    pass