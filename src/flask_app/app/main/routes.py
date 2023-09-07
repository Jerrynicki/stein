import flask
from app.main import bp
from app.models import user

@bp.route("/")
def index():
    # users = user.User.query.all()
    # a = "\n".join([x.name + " " + str(x.admin) for x in users])
    return flask.render_template("index.html")