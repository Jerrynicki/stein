from app.extensions import db

class Token(db.Model):
    token = db.Column(db.String(length=36), primary_key=True) # max length = 36
    expiry = db.Column(db.Integer)
    user_id = db.Column(db.ForeignKey("user.id"))
    post = db.relationship("User")