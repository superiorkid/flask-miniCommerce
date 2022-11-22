import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    DEBUG = False
    SECRET_KEY = os.urandom(16)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


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
