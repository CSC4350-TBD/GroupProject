from flask import Flask
from flask_login import LoginManager

# from sqlalchemy.ext.declarative.api import declarative_base
from wtforms import Form, TextField, PasswordField, validators, BooleanField
from flask_login import login_user, logout_user, current_user, login_required, UserMixin
from app import db, app  # app will be the app to run the initialization
from model import User, saved_movies, genre_exclusions, ignored_movies
import requests
from flask import render_template, flash, redirect, url_for, request
from form import LoginForm, RegistrationForm
import flask
import os
from flask_sqlalchemy import SQLAlchemy
from moviedb import get_detailed_info, get_id, get_movie_info
from imdb import get_imdb_id
from recommend import get_recommendation

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/")
@app.route("/index")
@login_required
def index():

    # main page here
    return render_template("index.html")


# The following will probably need to be split between diffent pages, depending on how we do the routing.
# This just made it easy to make sure that the APIs work.
@app.route("/searchMovie", methods=["GET", "POST"])
def main():
    search_term = request.form["search"]
    # try:
    # imdbid, imdb_api_img = get_imdb_id(search_term)
    # moviedb_id = get_id(imdbid)
    # movie_genre, movie_title = get_movie_info(moviedb_id)
    rec_list = get_recommendation(search_term)
    title_list = []
    title_list_len = 10
    for i in rec_list:
        genre, title = get_movie_info(i)
        title_list.append(title)
    title_list_len = len(title_list)

    # except Exception:
    # flask.flash("Invalid movie name entered")
    # return flask.redirect(flask.url_for("index"))
    return flask.render_template(
        "index.html",
        search_term=search_term,
        # imdb_api_img=imdb_api_img,
        # movie_title=movie_title,
        # movie_genre=movie_genre,
        title_list=title_list,
        title_list_len=title_list_len,
        rec_list=rec_list,
    )


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
        if User.query.filter_by(username=form.username.data).first():
            flash("The user name already exist, please try a new one.")
            return redirect(url_for("register"))
        db.session.add(user)
        db.session.commit()
        # print(user)
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/user", methods=["GET", "POST"])
def user():
    usename = current_user.username
    saved_movies_list = [
        r[0]
        for r in db.session.query(saved_movies.movieid)
        .filter_by(usename=usename)
        .distinct()
    ]
    ignored_movies_list = [
        r[0]
        for r in db.session.query(ignored_movies.ignoredmovieid)
        .filter_by(usename=usename)
        .distinct()
    ]
    # function need to be added for removing from database
    # removing: removing saved movies or ignored movies
    print("insuerinuser")
    print(saved_movies_list)
    print("insuerinuser")
    print("insuerinuser")

    return render_template(
        "user.html",
        saved_movies_list=saved_movies_list,
        ignored_movies_list=ignored_movies_list,
    )


@app.route("/details", methods=["GET", "POST"])
def details():
    immdict = request.form.to_dict()
    movie_id = list(immdict.values())
    for key, value in immdict.items():
        movie_id = key
    (
        movie_title,
        movie_img,
        movie_genre,
        movie_desc,
        movie_runtime,
        movie_rating,
        cast,
        director,
    ) = get_detailed_info(movie_id)

    return render_template(
        "details.html",
        movie_id=movie_id,
        movie_title=movie_title,
        movie_img=movie_img,
        movie_genre=movie_genre,
        movie_desc=movie_desc,
        movie_runtime=movie_runtime,
        movie_rating=movie_rating,
        cast=cast,
        director=director,
    )


@app.route("/save", methods=["GET", "POST"])
def save():
    immdict = request.form.to_dict()
    movie_id = list(immdict.values())
    for key, value in immdict.items():
        movie_id = key
    # save to watch
    # if movie_id ! in database:
    usename = current_user.username
    db.session.add(saved_movies(movieid=movie_id, usename=usename))
    db.session.commit()
    flash("Saved!")
    return render_template("index.html", movie_id=movie_id)


@app.route("/ignore", methods=["GET", "POST"])
def ignore():
    immdict = request.form.to_dict()
    movie_id = list(immdict.values())
    for key, value in immdict.items():
        movie_id = key
    usename = current_user.username
    db.session.add(ignored_movies(ignoredmovieid=movie_id, usename=usename))
    db.session.commit()
    return render_template("index.html", movie_id=movie_id)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(
        # uncomment following 2 lines once ready for deployment to heroku.
        # host=os.getenv("IP", "0.0.0.0"),
        # port=int(os.getenv("PORT", 8080)),
        debug=True,
    )
