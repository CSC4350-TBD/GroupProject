import flask
import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv
from flask_mail import Mail
from flask_login import UserMixin

load_dotenv(find_dotenv())

load_dotenv(find_dotenv())

app = flask.Flask(__name__)
app.config.update(
    DEBUG = True,
    MAIL_SERVER = 'smtp.office365.com',
    MAIL_PORT = 587, #outlook smtp port number
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD'),
    MAIL_DEBUG = True,
)
mail = Mail(app)
# Heroku DB Fix incase of bad db url
db_url = os.getenv("DATABASE_URL")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url

# Gets rid of a warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = b"I am a secret key!"  # don't defraud my app ok?
app.config["SQLALCHEMY_ECHO"] = True


db = SQLAlchemy(app)
