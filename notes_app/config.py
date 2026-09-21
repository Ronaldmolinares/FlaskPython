import os

DB_FILE_PATH = os.path.join(os.path.dirname(__file__), "notes.sqlite")


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "flask-notes-secret-key")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_FILE_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///test_notes.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "flask-notes-secret-key")
    TESTING = True
