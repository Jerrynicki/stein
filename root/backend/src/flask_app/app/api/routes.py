import flask

import hashlib
import secrets
import base64

from app.api import bp
import app.models as models
import app.dbh.dbhelper as dbh

import app.util as util

@bp.route("/login", methods=["POST"])
def login():
    req = flask.request.get_json()

    if not all(req["username"], req["password"]):
        return "", 400

    if dbh.validate_login(req["username"], req["password"]):
        # Login valid
        user = dbh.get_user(req["username"])
        token = dbh.create_token(user)
        return {
            token: token.token,
            expiry: token.expiry
        }, 200
    else:
        # Login invalid
        return "Invalid login", 403

@bp.route("/register", methods=["POST"])
def register():
    req = flask.request.get_json()
    
    teams = dbh.get_teams()

    team_valid = False
    for team in teams:
        if team.id == req["team"]:
            team_valid = True

    if not team_valid:
        return "Invalid team", 400

    new_user = models.user.User()

    new_user.admin = False
    new_user.banned = False

    name_unique = False
    while not name_unique:
        new_user.name = util.name_generator.generate_username()
        if dbh.get_user(new_user.name) is None:
            name_unique = True

    new_user.password_salt = secrets.token_bytes(16)
    new_user.password_hash = hashlib.sha256(
        req["password"].encode("utf8") + new_user.password_salt
    ).digest()

    dbh.create_user(new_user)

    token = dbh.create_token(new_user)

    return {
        "username": new_user.name,
        "token": token.token,
        "expiry": token.expiry
    }, 200

@bp.route("/post", methods=["POST"])
def post_post():
    user = util.auth.user_from_request(flask.request)

    if user is None:
        return "", 401

    req = flask.request.get_json()

    if req["location_lat"] < -180 or req["location_lat"] > 180 \
        or \
    req["location_lon"] < -180 or req["location_lon"] > 180:
        return "Longitude/Latitude format invalid", 400

    post = models.post.Post()
    post.author = user.name
    post.location_lat = req["location_lat"]
    post.location_lon = req["location_lon"]
    post.image = base64.b64decode(req["image"]) ## TODO image processing

    post.create()

    id = post.id
    # id = dbh.create_post(post)

    return {"id": id}, 200

@bp.route("/post", methods=["GET"])
def get_post():
    assert flask.request.args["id"]

    post_id = int(flask.request.args["id"])

    p = dbh.get_post(post_id)

    return {
        "id": p.id,
        "author": p.author,
        "image_url": util.image_url.get_post_image_url(post_id)
    }, 200