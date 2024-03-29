from flask import Flask
from flask_bootstrap import Bootstrap4
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from flask_ckeditor import CKEditor
from flask_cors import CORS
from flask_toastr import Toastr
from flask_session import Session

from config import DevelopmentConfig
from .errors import error_handlers
from .utility.jinja2_filter.global_filter import filter_list

bootstrap = Bootstrap4()
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
ckeditor = CKEditor()
cors = CORS()
toastr = Toastr()
sess = Session()

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
    cors.init_app(app)
    toastr.init_app(app)
    sess.init_app(app)

    # import blueprint
    from .auth import auth as auth_blueprint
    from .products import products as product_blueprint
    from .main import main as main_blueprint
    from .users import users as users_blueprint
    from .cart import cart as cart_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(product_blueprint, url_prefix="/product")
    app.register_blueprint(users_blueprint, url_prefix="/users")
    app.register_blueprint(cart_blueprint, url_prefix="/cart")

    # error blueprint
    error_handlers(app, db)

    # jinja2 global filter
    filter_list(app)

    return app
