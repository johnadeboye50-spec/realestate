import os

class GeneralConfig:
    ADMIN_EMAIL = "johnadeboye50@gmail.com"

class TestingConfig(GeneralConfig):
    SQLALCHEMY_DATABASE_URI = (
        "mysql+mysqlconnector://root:Johnperry144@localhost:3307/realestate_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LiveConfig(GeneralConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Johnperry144@localhost:3307/realestate_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False