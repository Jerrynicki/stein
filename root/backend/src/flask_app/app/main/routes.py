import os

import flask
import werkzeug
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
    frontend_path = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../dist/styn/browser"))

    if os.path.exists(os.path.join(frontend_path, path)):
        result = flask.send_from_directory(
            frontend_path,
            path
        )
    else:
        result = flask.send_from_directory(
            frontend_path,
            "index.html"
        )

    return result