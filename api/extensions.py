from flask import redirect, request, url_for
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()


def init_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    from api.models import User

    return db.session.get(User, int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    if request.path.endswith("_fr"):
        return redirect(url_for("auth.login_fr"))
    return redirect(url_for("auth.login"))
