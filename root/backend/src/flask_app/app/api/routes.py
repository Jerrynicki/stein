import flask

from app.main import bp
import app.models as models
import app.dbh.dbhelper as dbh

@bp.route("/login", methods=["POST"])
def login():
    req = flask.request.get_json()
    if dbh.validate_login(req.username, req.password):
        # Login valid
        user = dbh.get_user(req.username)
        token = dbh.create_token(user)
        return {
            token: token.token,
            expiry: token.expiry
        }, 200
    else:
        # Login invalid
        return "Invalid login", 403