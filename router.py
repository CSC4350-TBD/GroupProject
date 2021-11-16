from flask import Flask
from flask_login import LoginManager
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
from moviedb import get_id, get_movie_info
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
    search_term = request.form['search']
<<<<<<< HEAD
    title_list = []
    try:
        (imdbid, imdb_api_img) = get_imdb_id(search_term)
        moviedb_id = get_id(imdbid)
        (movie_genre, movie_title) = get_movie_info(moviedb_id)
        rec_list = get_recommendation(search_term)
        rec_list_len = len(rec_list)
        # for i in rec_list_len:
        #     movie_title = get_movie_info(i)
        #     title_list.append(movie_title)
        
            
    except Exception:
        flask.flash("Invalid movie name entered")
        return flask.redirect(flask.url_for("index"))
    return flask.render_template("index.html", imdb_api_img=imdb_api_img, movie_title=movie_title, movie_genre=movie_genre,rec_list_len=rec_list_len)
=======
    #try:
    #imdbid, imdb_api_img = get_imdb_id(search_term)
    #moviedb_id = get_id(imdbid)
    #movie_genre, movie_title = get_movie_info(moviedb_id)
    rec_list = get_recommendation(search_term)
    title_list = []
    title_list_len=10
    for i in rec_list:
        genre, title = get_movie_info(i)
        title_list.append(title)
    title_list_len = len(title_list)
    print(search_term)
    print(rec_list)
    print(title_list)
    print("THIS IS TO MAKE SURE THE PRINT WORKS")
    print("THIS IS TO MAKE SURE THE PRINT WORKS")
    print("THIS IS TO MAKE SURE THE PRINT WORKS")
    print("THIS IS TO MAKE SURE THE PRINT WORKS")
    print("THIS IS TO MAKE SURE THE PRINT WORKS")
    print("THIS IS TO MAKE SURE THE PRINT WORKS")
    print("THIS IS TO MAKE SURE THE PRINT WORKS")
    print("THIS IS TO MAKE SURE THE PRINT WORKS")

    #except Exception:
        #flask.flash("Invalid movie name entered")
        #return flask.redirect(flask.url_for("index"))
    return flask.render_template("index.html",
        search_term=search_term, 
        #imdb_api_img=imdb_api_img, 
        #movie_title=movie_title, 
        #movie_genre=movie_genre,
        title_list=title_list,
        title_list_len=title_list_len)
>>>>>>> 7153cc3ba74ce8a09d838dba437a216eabf77047
     
     

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
<<<<<<< HEAD
        # host=os.getenv("IP", "0.0.0.0"),
        # port=int(os.getenv("PORT", 8080)),
=======
        #host=os.getenv("IP", "0.0.0.0"),
        #port=int(os.getenv("PORT", 8080)),
>>>>>>> 7153cc3ba74ce8a09d838dba437a216eabf77047
        debug=True,
    )
