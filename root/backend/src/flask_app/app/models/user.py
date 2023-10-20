from app.extensions import db

class User(db.Model):
    name = db.Column(db.String(length=36), primary_key=True) # max length = 36
    password_hash = db.Column(db.BLOB(length=64)) # sha 256 hash
    password_salt = db.Column(db.BLOB(length=16)) # length 16
    admin = db.Column(db.Boolean)
    banned = db.Column(db.Boolean)
    team = db.Column(db.ForeignKey("team.id"))