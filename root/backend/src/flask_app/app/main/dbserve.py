import flask
from app.main import bp

import app.models as models
from app.extensions import db

import app.dbh.dbhelper as dbh

@bp.route("/dbstatic/<path:path>")
def dbstatic(path):
    # see util/image_url.py

    path = path.split("/")

    if path[0] == "images":
        if path[1] == "post":
            image = dbh.get(models.post_picture.PostPicture, models.post_picture.PostPicture.id, int(path[2]))
        
            if image is None == 0:
                return "Not found", 404

            response = flask.make_response(image.image)
            response.headers.set("Content-Type", image.mimetype)

            return response
        elif path[1] == "user":
            profile_pic = dbh.get(models.profile_picture.ProfilePicture, models.profile_picture.ProfilePicture.user, path[2])

            if profile_pic is None:
                return "Not found", 404

            response = flask.make_response(profile_pic.image)
            response.headers.set("Content-Type", profile_pic.mimetype)

            return response

    return "Not found", 404