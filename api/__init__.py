from flask import Flask

from api.blueprints.auth import auth_bp
from api.blueprints.dashboard import dashboard_bp
from api.blueprints.main import main_bp
from api.config import BaseConfig
from api.extensions import init_extensions
from api.extensions import db


def create_app(test_config=None):
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(BaseConfig)

    if test_config:
        app.config.update(test_config)

    init_extensions(app)
    register_blueprints(app)
    register_database_hook(app)
    return app


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)


def register_database_hook(app):
    app.extensions["tables_initialized"] = False

    @app.before_request
    def initialize_database():
        if app.config.get("TESTING") or app.extensions["tables_initialized"]:
            return

        with app.app_context():
            db.create_all()

        app.extensions["tables_initialized"] = True
