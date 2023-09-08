from app.extensions import db
from . import post

class Comment(db.Model):
    post_id = db.Column(db.ForeignKey("post.id"))
    post = db.relationship("Post")
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.ForeignKey("user.name"))
    comment = db.Column(db.Unicode(length=3))
    rating = db.Column(db.Integer)
    removed = db.Column(db.Boolean)