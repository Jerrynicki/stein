import flask
import os
import json

from flask_cors import CORS

from app.extensions import db

CONFIG_LOCATION = os.path.abspath(os.path.dirname(__file__)) + "/stein.json"

def create_app():
    """App constructor"""

    app = flask.Flask(__name__)
    CORS(app) # needed for swagger

    # app.config.from_object(cfg.get_flask_config())
    app.config.from_file(CONFIG_LOCATION, load=json.load)

    db.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()

        if app.debug:
            # ensure that a team always exists
            # after the db was reset
            # (it less annoying)
            import app.dbh.dbhelper as dbh
            if len(dbh.all(models.team.Team)) == 0:
                t = models.team.Team()
                t.id = -1
                t.name = "stein-debugger"
                t.color = "#69420a"
                dbh.create(t)

    return app