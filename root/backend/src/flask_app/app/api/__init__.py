import flask

bp = flask.Blueprint("api", __name__)

from app.api import routes