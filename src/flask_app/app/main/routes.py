import flask
from app.main import bp

import app.models as models
from app.extensions import db

@bp.route("/")
def index():
    # users = user.User.query.all()
    # a = "\n".join([x.name + " " + str(x.admin) for x in users])

    u = models.user.User(
        name = "gamer69",
        admin = True,
        banned = False
    )

    db.session.add(u)

    p = models.post.Post(
        author = u.name,
        image = b"\x01\x03",
        location_lat = 52.3912,
        location_lon = 12.3413,
        removed = False
    )

    db.session.add(p)
    db.session.flush()


    print(p.id)

    c = models.comment.Comment(
        post_id = p.id,
        author = u.name,
        comment = "ABC",
        rating = 5,
        removed = False
    )

    db.session.add(c)

    db.session.commit()

    #db.insert(model.comment.Comment).values(
    #    post_id = 
    #)
    
    return flask.render_template("index.html")