import os

import flask
from app.main import bp

import app.models as models
from app.extensions import db

# this file is currently a stub in case any other routes need to be
# added in the future

# see stein.json for configuration of frontend location
# see api module for the api routes

@bp.route("/")
@bp.route("/<path:path>")
def frontend(path="index.html"):
    return flask.send_from_directory(
        os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../../../../frontend/stein_app/dist/stein_app")),
        path
    )