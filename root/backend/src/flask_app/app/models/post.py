from app.extensions import db

from sqlalchemy.orm import relationship

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.ForeignKey("user.name"))
    timestamp = db.Column(db.Integer)
    location_lat = db.Column(db.Float) # latitude N
    location_lon = db.Column(db.Float) # longitude E
    removed = db.Column(db.Boolean)
    rating = db.Column(db.Float) # average rating, cached. needs to be updated if a new comment is submitted