from app.extensions import db

from sqlalchemy.orm import relationship

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    color = db.Column(db.String(length=6))