from app.extensions import db
from . import post

class Comment(db.Model):
    post_id = db.Column(db.ForeignKey("post.id"))
    post = db.relationship("Post")
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.ForeignKey("user.name"))
    comment = db.Column(db.Unicode(length=3))
    timestamp = db.Column(db.Integer)
    location_lat = db.Column(db.Float) # latitude N
    location_lon = db.Column(db.Float) # longitude E
    rating = db.Column(db.Integer)
    
    removed = db.Column(db.Boolean, default=False)
    edited = db.Column(db.Boolean, default=False)
    edited_followup = db.Column(db.Integer) # the id of the next comment