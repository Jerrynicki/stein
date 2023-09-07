from app.extensions import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image = db.Column(db.BLOB)
    location_lat = db.Column(db.Float) # latitude N
    location_lon = db.Column(db.Float) # longitude E
    removed = db.Column(db.Boolean)
    author = db.ForeignKey("user.name")