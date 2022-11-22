from flask import Flask
from flask_bootstrap import Bootstrap4
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from config import DevelopmentConfig
from .errors import error_handlers

bootstrap = Bootstrap4()
db = SQLAlchemy()
migrate = Migrate()

login_manager = LoginManager()
login_manager.login_view = "auth.signin"


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db, compare_type=True)

    # import blueprint
    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint

    # register blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(main_blueprint)

    # error blueprint
    error_handlers(app, db)

    return app
