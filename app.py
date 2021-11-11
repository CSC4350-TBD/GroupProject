import flask
import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

load_dotenv(find_dotenv())

app = flask.Flask(__name__)


# Heroku DB Fix incase of bad db url
db_url = os.getenv("DATABASE_URL")
if db_url.startswith("postgres://"):
	db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URL"] = db_url

# Gets rid of a warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = b'I am a secret key!'  # don't defraud my app ok?
app.config['SQLALCHEMY_ECHO'] = True
from flask_login import UserMixin

db = SQLAlchemy(app)
