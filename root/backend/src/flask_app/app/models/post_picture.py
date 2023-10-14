from app.extensions import db

class PostPicture(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.ForeignKey("post.id"))
    post = db.relationship("Post")
    image = db.Column(db.BLOB)
    quality_level = db.Column(db.Integer)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    mimetype = db.Column(db.String)