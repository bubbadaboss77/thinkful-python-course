import os

class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://ubuntu:thinkful@localhost:5432/textbook"
    DEBUG = True
    SECRET_KEY = os.environ.get("TEXTBOOK_SECRET_KEY", os.urandom(12))