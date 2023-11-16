import os


class Config:
    # if you are going to upload the secret_key and uri of database then store them in your environment variables and not like this openly in editor
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("USER_G_SKUKKA744")
    MAIL_PASSWORD = os.environ.get("PASS_G_SKUKKA744")
