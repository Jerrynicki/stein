from app.extensions import db

TOKEN_LENGTH = 36

class Token(db.Model):
    token = db.Column(db.String(length=TOKEN_LENGTH), primary_key=True) # max length = 36
    expiry = db.Column(db.Integer)
    username = db.Column(db.ForeignKey("user.name"))
    user = db.relationship("User")