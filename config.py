import os
import redis

from dotenv import load_dotenv

load_dotenv()

basedir = os.getcwd()


class Config(object):

    DEBUG = False
    SECRET_KEY = os.urandom(16)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # EMAIL
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = "mailtestingforstudy@gmail.com"
    MAIL_PASSWORD = 'oqrgqffrjsrstayx'

    # theme
    BOOTSTRAP_BOOTSWATCH_THEME = 'sandstone'

    # ckeditor
    CKEDITOR_PKG_TYPE = "basic"

    # storing file upload
    UPLOAD_FOLDER = os.path.join(basedir, 'app/static/uploads')

    # toastr
    TOASTR_POSITION_CLASS = "toast-bottom-right"

    # session
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url('redis://localhost:6379')


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    IS_ADMIN = os.getenv("IS_ADMIN")


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI_DEV")
    IS_ADMIN = os.getenv("IS_ADMIN_DEV")

    # MIDTRANS INTEGRATION
    SERVER_KEY = os.getenv('MIDTRANS_SERVER_KEY')
    CLIENT_KEY = os.getenv('MIDTRANS_CLIENT_KEY')

    # RAJAONGKIR
    KEY = os.getenv('RAJAONGKIR_KEY')
