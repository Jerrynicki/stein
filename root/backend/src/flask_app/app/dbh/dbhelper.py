import sqlalchemy
from app.extensions import db
import app.models as models

from app.extensions import db

def create(model):
    db.session.add(model)
    db.session.flush()
    db.session.commit()

def get(model, field, value):
    return db.session.execute(
        sqlalchemy.select(
            model
        ).where(
            field == value
        )
    ).scalar_one_or_none()

def query(model, expression):
    return db.session.execute(
        sqlalchemy.select(
            model
        ).where(
            expression
        )
    ).scalars()

def delete(model, expression):
    db.session.execute(
        sqlalchemy.delete(
            model
        ).where(
            expression
        )
    )
    db.session.flush()
    db.session.commit()

def all(model):
    return db.session.execute(sqlalchemy.select(model)).scalars()
