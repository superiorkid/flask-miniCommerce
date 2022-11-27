from flask import Flask
from flask_bootstrap import Bootstrap4
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from flask_ckeditor import CKEditor

from config import DevelopmentConfig
from .errors import error_handlers

bootstrap = Bootstrap4()
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
ckeditor = CKEditor()

login_manager = LoginManager()
login_manager.login_view = "auth.signin"


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    mail.init_app(app)
    ckeditor.init_app(app)

    # jinja global filter
    @app.template_filter()
    def currency_format(value):
        return format(int(value), ',d')

    # import blueprint
    from .auth import auth as auth_blueprint
    from .products import products as product_blueprint
    from .main import main as main_blueprint
    from .admin import admin as admin_blueprint

    # register blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(product_blueprint, url_prefix="/product")
    app.register_blueprint(admin_blueprint, url_prefix="/admin")

    # error blueprint
    error_handlers(app, db)

    return app
