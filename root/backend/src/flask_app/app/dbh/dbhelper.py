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

def get_multiple(model, field, value):
    return db.session.execute(
        sqlalchemy.select(
            model
        ).where(
            field == value
        )
    ).scalars().all()

def query(model, expression):
    return db.session.execute(
        sqlalchemy.select(
            model
        ).where(
            expression
        )
    ).scalars().all()

def delete(model):
    db.session.remove(model)
    db.session.flush()
    db.session.commit()

def delete_expression(model, expression):
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
    return db.session.execute(
        sqlalchemy.select(
            model
        )
    ).scalars().all()

def flcm():
    """flush and commit"""
    db.session.flush()
    db.session.commit()