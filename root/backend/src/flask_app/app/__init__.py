import flask
import os
import json

from app.extensions import db

CONFIG_LOCATION = os.path.abspath(os.path.dirname(__file__)) + "/stein.json"

def create_app():
    """App constructor"""

    app = flask.Flask(__name__)

    # app.config.from_object(cfg.get_flask_config())
    app.config.from_file(CONFIG_LOCATION, load=json.load)

    db.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api import bs as api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()

    return app