import flask
import sqlalchemy

import hashlib
import secrets
import base64
import time

from app.api import bp
from app.extensions import db
import app.models as models
import app.dbh.dbhelper as dbh

import app.util as util

@bp.route("/login", methods=["POST"])
def login():
    req = flask.request.get_json()

    if not util.request.check_fields(req, ["username", "password"]):
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

    if not util.request.check_fields(req, ["team", "password"]):
        return "", 400
    
    teams = dbh.all(models.team.Team)

    team_valid = False
    for team in teams:
        if team.id == int(req["team"]):
            team_valid = True

    if not team_valid:
        return "Invalid team", 400

    new_user = models.user.User()

    new_user.admin = False
    new_user.banned = False
    new_user.team = int(req["team"])

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

    if not util.request.check_fields(req,
        ["location_lat", "location_lon", "image"]):
        return "", 400

    if req["location_lat"] < -180 or req["location_lat"] > 180 \
        or \
    req["location_lon"] < -180 or req["location_lon"] > 180:
        return "Longitude/Latitude format invalid", 400

    # Create post
    post = models.post.Post()
    post.author = user.name
    post.timestamp = int(time.time())
    post.location_lat = req["location_lat"]
    post.location_lon = req["location_lon"]

    dbh.create(post)

    # Image processing and create images
    image_raw = base64.b64decode(req["image"])
    images = util.image.to_post_pictures(
        image_raw,
        post.id
    )

    for i in images:
        dbh.create(i)

    # Check if user has profile picture and set as picture if they don't
    if util.image_url.get_profile_image_url(user.name) is None:
        profile_pic = util.image.to_profile_picture(image_raw, user.name)
        dbh.create(profile_pic)

    return {"id": post.id}, 200

@bp.route("/post", methods=["GET"])
def post_get():
    if not util.request.check_fields(flask.request.args, ["id"]):
        return "", 400

    post_id = int(flask.request.args["id"])

    p = dbh.get(models.post.Post, models.post.Post.id, post_id)

    if p is None or p.removed:
        return "", 404
    else:
        return {
            "id": p.id,
            "author": p.author,
            "images": util.image_url.get_post_images(post_id)
        }, 200

@bp.route("/post", methods=["DELETE"])
def post_delete():
    if not util.request.check_fields(flask.request.args, ["id"]):
        return "", 400

    post_id = int(flask.request.args["id"])

    u = util.auth.user_from_request(flask.request)

    if u is None:
        return "Unauthorized", 403

    p = dbh.get(models.post.Post, models.post.Post.id, post_id)

    if p is None or p.removed:
        return "", 404
    
    if p.author == u.name:
        p.removed = True
        dbh.flcm()
        return "", 200
    else:
        return "", 401

@bp.route("/post/comments", methods=["GET"])
def post_comments_get():
    if not util.request.check_fields(flask.request.args, ["id"]):
        return "", 400

    post_id = int(flask.request.args["id"])
    post = dbh.get(models.post.Post, models.post.Post.id, post_id)

    if post is None or post.removed:
        return "Post not found", 404

    comments = dbh.get_multiple(models.comment.Comment, models.comment.Comment.post_id, post_id)

    response = []

    for c in comments:
        if not c.removed and not c.edited:
            dist = util.coords.distance_between_coords(
                post.location_lat,
                post.location_lon,
                c.location_lat,
                c.location_lon
            )
            response.append(
                {
                    "id": c.id,
                    "author": c.author,
                    "comment": c.comment,
                    "timestamp": c.timestamp,
                    "distance": int(dist),
                    "rating": c.rating,
                }
            )

    return response, 200

@bp.route("/post/comments", methods=["POST", "PUT"])
def post_comments_post_put():
    req = flask.request.get_json()

    if not util.request.check_fields(flask.request.args, ["id"]):
        return "", 400
    if flask.request.method == "POST":
        if not util.request.check_fields(req, ["location_lon", "location_lat", "rating", "comment"]):
            return "", 400
    if flask.request.method == "PUT":
        if not util.request.check_fields(req, ["id", "rating", "comment"]):
            return "", 400

    post_id = int(flask.request.args["id"])

    post = dbh.get(models.post.Post, models.post.Post.id, post_id)
    if post is None:
        return "Post not found", 404

    author = util.auth.user_from_request(flask.request)

    if author is None:
        return "", 403

    comment = models.comment.Comment()
    comment.author = author.name
    comment.comment = req["comment"]
    comment.post_id = post_id
    comment.rating = req["rating"]
    comment.removed = False
    comment.timestamp = int(time.time())

    if flask.request.method == "POST":
        comment.location_lat = req["location_lat"]
        comment.location_lon = req["location_lon"]
        dbh.create(comment)
    if flask.request.method == "PUT":
        # set the old comment to status edited with a reference to the new comment
        old_comment = dbh.get(models.comment.Comment, models.comment.Comment.id, req["id"])
        if old_comment is None or old_comment.removed:
            return "Comment not found", 404
        if old_comment.author != author.name and not author.admin:
            return "", 401
        if old_comment.edited:
            return "Comment has already been edited", 404

        comment.location_lat = old_comment.location_lat
        comment.location_lon = old_comment.location_lon
        dbh.create(comment)

        old_comment.edited = True
        old_comment.edited_followup = comment.id
        dbh.flcm()

    return {"id": comment.id}, 200

@bp.route("/post/comments", methods=["DELETE"])
def post_comments_delete():
    if not util.request.check_fields(flask.request.args, ["id", "comment_id"]):
        return "", 400

    comment_id = int(flask.request.args["comment_id"])
    post_id = int(flask.request.args["id"])

    u = util.auth.user_from_request(flask.request)

    if u is None:
        return "Unauthorized", 403

    c = dbh.get(models.comment.Comment, models.comment.Comment.id, comment_id)

    if c is None or c.removed or c.edited:
        return "", 404
    
    if c.author == u.name:
        c.removed = True
        dbh.flcm()
        return "", 200
    else:
        return "", 401

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

@bp.route("/profile", methods=["GET"])
def profile_get():
    if not util.request.check_fields(flask.request.args, ["name"]):
        return "", 400

    username = flask.request.args["name"]
    user = dbh.get(models.user.User, models.user.User.name, username)

    if user is None:
        return "User not found", 404

    return {
        "name": user.name,
        "profile_picture_url": util.image_url.get_profile_image_url(username),
        "admin": user.admin,
        "banned": user.banned,
        "team": user.team
    }, 200

@bp.route("/profile/posts", methods=["GET"])
def profile_posts_get():
    PAGE_SIZE = 50

    print(flask.request.args)
    if not util.request.check_fields(flask.request.args, ["name", "page"]):
        return "", 400

    username = flask.request.args["name"]
    page = int(flask.request.args["page"])

    user = dbh.get(models.user.User, models.user.User.name, username)
    if user is None:
        return "User not found", 404

    posts = db.session.execute(
        sqlalchemy.select(
            models.post.Post
        ).where(
            models.post.Post.author == username
        ).order_by(models.post.Post.timestamp.desc()
        ).limit(
            PAGE_SIZE
        ).offset(
            PAGE_SIZE * page
        )
    ).scalars().all()
    
    response = []
    for p in posts:
        response.append(
            {
                "id": p.id,
                "author": p.author,
                "images": util.image_url.get_post_images(p.id),
                "location_lat": p.location_lat,
                "location_lon": p.location_lon
            }
        )

    return response, 200

@bp.route("/posts", methods=["GET"])
def posts_get():
    # TODO caching

    PAGE_SIZE = 50

    OFFSET = 0.001 # ~112 meters start offset
    OFFSET_CHANGE = 2 # multiply by 2 on each operation
    TARGET_LEN = 1000 # find at least 1000 results

    if not util.request.check_fields(flask.request.args, ["page", "location_lat", "location_lon"]):
        return "", 400

    location_lat = float(flask.request.args["location_lat"])
    location_lon = float(flask.request.args["location_lon"])
    page = int(flask.request.args["page"])

    response = []

    results = []

    iteration = 0
    min_lon, max_lon, min_lat, max_lat = 0,0,0,0

    while len(results) < TARGET_LEN and \
        not (min_lon < -180 and max_lon > 180 and min_lat < -180 and max_lat > 180):

        min_lon = location_lon - OFFSET * (OFFSET_CHANGE**iteration)
        max_lon = location_lon + OFFSET * (OFFSET_CHANGE**iteration)
        min_lat = location_lat - OFFSET * (OFFSET_CHANGE**iteration)
        max_lat = location_lat + OFFSET * (OFFSET_CHANGE**iteration)
        
        start_time = time.time()
        results = db.session.execute(
            sqlalchemy.select(
                models.post.Post
            ).where(
                models.post.Post.location_lon >= min_lon,
                models.post.Post.location_lon <= max_lon,
                models.post.Post.location_lat >= min_lat,
                models.post.Post.location_lat <= max_lat,
                models.post.Post.removed == False or models.post.Post.removed == None
            )
        ).scalars().all()
        end_time = time.time()

        iteration += 1

    response = []
    for r in results:
        if not r.removed:
            response.append(
                {
                    "id": r.id,
                    "author": r.author,
                    "images": util.image_url.get_post_images(r.id),
                    "location_lat": r.location_lat,
                    "location_lon": r.location_lon,
                    "distance": int(util.coords.distance_between_coords(
                        location_lat, location_lon,
                        r.location_lat, r.location_lon
                    ))
                }
            )

    # sort by distance
    response = sorted(response, key=lambda k: k["distance"])

    return response[page*PAGE_SIZE:(page+1)*PAGE_SIZE], 200