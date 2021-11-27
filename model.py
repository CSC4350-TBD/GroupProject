from flask_login import login_user, logout_user, current_user, login_required, UserMixin
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from flask import current_app, url_for
from time import time


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64),index=True, unique=True)
    email = db.Column(db.String(120),index=True, unique=True)
    password_hash = db.Column(db.String(128))


    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_jwt_token(self, expires_in=600):
        #get json web token#
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in},
                          current_app.config['SECRET_KEY'],
                          algorithm='HS256').decode('utf8')
    
    @staticmethod
    def verify_jwt_token(token):
        try:
            id = jwt.decode(token, 
                                 current_app.config['SECRET_KEY'], 
                                 algorithms='HS256')['reset_password']
        except Exception as e:
            print(e)
            return
        return User.query.get(id)


class genre_exclusions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genreexclusion = db.Column(db.String(20), unique=True)
    usename = db.Column(db.String(64))


class saved_movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movieid = db.Column(db.String(20))
    usename = db.Column(db.String(64))


class ignored_movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ignoredmovieid = db.Column(db.String(20))
    usename = db.Column(db.String(64))


db.create_all()
