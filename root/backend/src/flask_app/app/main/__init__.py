import flask

bp = flask.Blueprint("main", __name__)

from app.main import routes
from app.main import dbserve