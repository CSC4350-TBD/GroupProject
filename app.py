import flask
import os
from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)
db = SQLAlchemy(app)

# Heroku DB Fix incase of bad db url
db_url = os.getenv("DATABASE_URL")
if db_url.startswith("postgres://"):
	db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url

# Gets rid of a warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.create_all()
from flask_login import UserMixin