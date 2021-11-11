from flask import Flask
from flask_login import LoginManager
from wtforms import Form, TextField, PasswordField, validators, BooleanField
from flask_login import login_user, logout_user, current_user, login_required, UserMixin
from app import db, app  # app will be the app to run the initialization
from model import User
import requests
from flask import render_template, flash, redirect, url_for, request
from form import LoginForm, RegistrationForm
import flask
import os
from flask_sqlalchemy import SQLAlchemy
from moviedb import get_id, get_movie_info
from imdb import get_imdb_id

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/")
@app.route("/index")
# @login_required
def index():
    # main page here
    return render_template("index.html")


# The following will probably need to be split between diffent pages, depending on how we do the routing.
# This just made it easy to make sure that the APIs work.
@app.route("/placeholder")
def main():
    search_term = "Dune"  # This will need to be changed into a form request later
    imdbid, imdb_api_img = get_imdb_id(search_term)
    moviedb_id = get_id(imdbid)
    movie_genre, movie_title = get_movie_info(moviedb_id)

    return flask.render_template("index.html")  # placeholder


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm(request.form)
    if form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("index"))
    return render_template("login.html", title="Sign In", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)
    # print(form.username.data)
    # print(form.password.data)
    if form.validate():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        # print(user)
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/user", methods=["GET", "POST"])
def user():
    # function need to be added for removing from database
    # removing: removing saved movies or ignored movies
    return render_template("user.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(
        # uncomment following 2 lines once ready for deployment to heroku.
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", 8080)),
        debug=True,
    )
