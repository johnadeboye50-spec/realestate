import os

class GeneralConfig:
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

class TestingConfig(GeneralConfig):
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LiveConfig(GeneralConfig):
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False