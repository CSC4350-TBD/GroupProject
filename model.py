from flask import Flask
from wtforms import Form,TextField,PasswordField,validators,BooleanField
from flask_login import login_user, logout_user, current_user, login_required,UserMixin
from app import db
from werkzeug.security import generate_password_hash, check_password_hash



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class genre_exclusions(db.model):
    id = db.Column(db.Integer, primary_key=True)
    genreexclusion = db.Column(db.String(20),unique=True)
    usename = db.Column(db.String(64))

class saved_movies(db.model):
    id = db.Column(db.Integer, primary_key=True)
    movieid = db.Column(db.String(20))
    usename = db.Column(db.String(64))

class ignored_movies(db.model):
    id = db.Column(db.Integer, primary_key=True)
    ignoredmovieid = db.Column(db.String(20))
    usename = db.Column(db.String(64))


db.create(all)
