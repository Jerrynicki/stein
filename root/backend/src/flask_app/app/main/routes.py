import flask
from app.main import bp

import app.models as models
from app.extensions import db


@bp.route("/")
def index():
    return flask.render_template("index.html")