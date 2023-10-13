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

    if not all([req["username"], req["password"]]):
        return "", 400

    if util.auth.validate_login(req["username"], req["password"]):
        # Login valid
        user = dbh.get(models.user.User, models.user.User.name, req["username"])
        token = util.auth.create_token(user)
        return {
            "token": token.token,
            "expiry": token.expiry
        }, 200
    else:
        # Login invalid
        return "Invalid login", 403

@bp.route("/register", methods=["POST"])
def register():
    req = flask.request.get_json()
    
    teams = dbh.all(models.team.Team)

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
        if dbh.get(models.user.User, models.user.User.name, new_user.name) is None:
            name_unique = True

    new_user.password_salt = secrets.token_bytes(16)
    new_user.password_hash = hashlib.sha256(
        req["password"].encode("utf8") + new_user.password_salt
    ).digest()

    dbh.create(new_user)

    token = util.auth.create_token(new_user)

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
    post.timestamp = int(time.time())
    post.location_lat = req["location_lat"]
    post.location_lon = req["location_lon"]
    post.image = base64.b64decode(req["image"]) ## TODO image processing

    dbh.create(post)

    id = post.id

    return {"id": id}, 200

@bp.route("/post", methods=["GET"])
def post_get():
    assert flask.request.args["id"]

    post_id = int(flask.request.args["id"])

    p = dbh.get(models.post.Post, models.post.Post.id, post_id)

    if p is None:
        return "", 404
    else:
        return {
            "id": p.id,
            "author": p.author,
            "image_url": util.image_url.get_post_image_url(post_id)
        }, 200

@bp.route("/post/comments", methods=["GET"])
def post_comments_get():
    assert flask.request.args["id"]

    post_id = int(flask.request.args["id"])

    comments = dbh.get_multiple(models.comment.Comment, models.comment.Comment.post_id, post_id)

    response = []

    for c in comments:
        if not c.removed and not c.edited:
            response.append(
                {
                    "id": c.id,
                    "author": c.author,
                    "comment": c.comment,
                    "timestamp": c.timestamp,
                    "location_lat": c.location_lat,
                    "location_lon": c.location_lon,
                    "rating": c.rating,
                }
            )

    return response, 200

@bp.route("/post/comments", methods=["POST", "PUT"])
def post_comments_post_put():
    assert flask.request.args["id"]

    post_id = int(flask.request.args["id"])

    post = dbh.get(models.post.Post, models.post.Post.id, post_id)
    if post is None:
        return "Post not found", 404

    author = util.auth.user_from_request(flask.request)

    if author is None:
        return "", 403

    req = flask.request.get_json()

    if not all([req["location_lat"], req["location_lon"], req["rating"], req["comment"]]):
        return "", 400

    comment = models.comment.Comment()
    comment.author = author.name
    comment.comment = req["comment"]
    comment.location_lat = req["location_lat"]
    comment.location_lon = req["location_lon"]
    comment.post_id = post_id
    comment.rating = req["rating"]
    comment.removed = False
    comment.timestamp = int(time.time())

    if request.method == "POST":
        dbh.create(comment)
    if request.method == "PUT":
        # set the old comment to status edited with a reference to the new comment
        old_comment = dbh.get(models.comment.Comment, models.comment.Comment.id, req["id"])
        if old_comment is None:
            return "Comment not found", 404
        if old_comment.author != author.name and not author.admin:
            return "", 401

        dbh.create(comment)

        old_comment.edited = True
        old_comment.edited_followup = comment.id
        dbh.flcm()

    return {"id": comment.id}, 200

@bp.route("/teams", methods=["GET"])
def teams_get():
    response = []

    teams = dbh.all(models.team.Team)

    print(teams)

    for t in teams:
        response.append(
            {
                "id": t.id,
                "name": t.name,
                "color": t.color
            }
        )

    return response, 200

