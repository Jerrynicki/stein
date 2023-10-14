from app.extensions import db

class ProfilePicture(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.ForeignKey("user.name"))
    user = db.relationship("User")
    image = db.Column(db.BLOB)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    mimetype = db.Column(db.String)