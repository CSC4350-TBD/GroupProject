from flask import Flask
from flask_login import LoginManager
from wtforms import Form, TextField, PasswordField, validators, BooleanField
from flask_login import login_user, logout_user, current_user, login_required, UserMixin
from app import db, app  # app will be the app to run the initialization
from model import User, saved_movies, genre_exclusions, ignored_movies, reviews
from app import db, app, mail  # app will be the app to run the initialization
from model import User, saved_movies, genre_exclusions, ignored_movies
import requests
import random
from flask import render_template, flash, redirect, url_for, request
from form import (
    LoginForm,
    RegistrationForm,
    ResetPasswordRequestForm,
    ResetPasswordForm,
)
import flask
import os
from flask_sqlalchemy import SQLAlchemy
from moviedb import (
    get_detailed_info,
    get_id,
    get_movie_info,
    get_movie_poster,
    get_movie_trailer,
)
from recommend import get_recommendation
from sendemail import send_password_reset_email


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
    rec_list, movie_img_url = get_recommendation(search_term)
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
        title_list=title_list,
        title_list_len=title_list_len,
        rec_list=rec_list,
        movie_img_url=movie_img_url,
    )


@app.route("/login", methods=["GET", "POST"])
def login():

    # choses a random movie quote and disply it on login page
    f = open("static/quotes.txt", "r")
    content = f.readlines()
    random_index = random.randint(0, len(content) - 1)
    random_quote = content[random_index]

    print(content[1])
    f.close()

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
    return render_template(
        "login.html", title="Sign In", form=form, random_quote=random_quote
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)
    print(form.email.data)
    print(type(form.email.data))
    if form.validate():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        if User.query.filter_by(username=form.username.data).first():
            flash("The user name already exist, please try a new one.")
            return redirect(url_for("register"))
        user.email = form.email.data
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


# request to reset password.
@app.route("/reset_request", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = ResetPasswordRequestForm(request.form)
    if form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash("this email is not regisited!")
            return redirect(url_for("reset_request"))
        send_password_reset_email(user)
        flash("please check your email to reset your password!")
        return redirect(url_for("login"))
    return render_template(
        "reset_password_request.html", title="reset password", form=form
    )


# reset password
@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    user = User.verify_jwt_token(token)
    if user is None:
        return redirect(url_for("index"))
    form = ResetPasswordForm(request.form)
    if form.validate():
        if user.check_password(form.password.data):
            flash('New password should be different with the old password')
            return redirect(url_for('reset_password',token=token))
        user.set_password(form.password.data)
        db.session.commit()
        flash("Your password reset successfully!")
        return redirect(url_for("login"))
    return render_template("reset.html", token=token, form=form)


@app.route("/user", methods=["GET", "POST"])
def user():

    return render_template(
        "user.html",
    )


@app.route("/user_saved_movies", methods=["GET", "POST"])
def user_saved_movies():
    usename = current_user.username
    saved_movies_list_titles = []
    saved_movie_imgs = []
    saved_movie_desc = []
    saved_movies_list = [
        r[0]
        for r in db.session.query(saved_movies.movieid)
        .filter_by(usename=usename)
        .distinct()
    ]

    for i in saved_movies_list:
        temp1, temp2 = get_movie_info(i)
        saved_movies_list_titles.append(temp2)
        saved_movie_img = get_movie_poster(i)
        saved_movie_imgs.append(saved_movie_img)
        (
            movie_title,
            movie_img,
            movie_genre,
            movie_desc,
            movie_runtime,
            movie_rating,
            cast,
            director,
        ) = get_detailed_info(i)
        saved_movie_desc.append(movie_desc)

    return render_template(
        "user_saved_movies.html",
        saved_movies_list_titles=saved_movies_list_titles,
        saved_movie_imgs=saved_movie_imgs,
        saved_movies_list=saved_movies_list,
        saved_movie_desc=saved_movie_desc,
    )


@app.route("/user_ignored_movies", methods=["GET", "POST"])
def user_ignored_movies():
    usename = current_user.username
    ignored_movies_list_titles = []
    ignored_movie_imgs = []
    ignored_movie_desc = []
    ignored_movies_list = [
        r[0]
        for r in db.session.query(ignored_movies.ignoredmovieid)
        .filter_by(usename=usename)
        .distinct()
    ]

    for i in ignored_movies_list:
        temp1, temp2 = get_movie_info(i)
        ignored_movies_list_titles.append(temp2)
        ignored_movie_img = get_movie_poster(i)
        ignored_movie_imgs.append(ignored_movie_img)
        print(ignored_movie_img)
        (
            movie_title,
            movie_img,
            movie_genre,
            movie_desc,
            movie_runtime,
            movie_rating,
            cast,
            director,
        ) = get_detailed_info(i)
        ignored_movie_desc.append(movie_desc)

    return render_template(
        "user_ignored_movies.html",
        ignored_movies_list_titles=ignored_movies_list_titles,
        ignored_movie_imgs=ignored_movie_imgs,
        ignored_movies_list=ignored_movies_list,
        ignored_movie_desc=ignored_movie_desc,
    )


@app.route("/details", methods=["GET", "POST"])
def details():
    # this is a very abnormal way to get this data passed, we are kind of exploiting how HTML is structured to pass varriables
    # this scales very poorly, but it works in this case.
    immdict = request.form.to_dict()
    movie_id = list(immdict.values())
    for key, value in immdict.items():
        movie_id = key
    return get_details(movie_id)


def get_details(movie_id):
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
    reviews = get_reviews_from_db(movie_id)

    trailer_url = get_movie_trailer(movie_id)

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
        reviews=reviews,
        trailer_url=trailer_url,
    )


@app.route("/save", methods=["GET", "POST"])
def save():
    immdict = request.form.to_dict()
    movie_id = list(immdict.values())
    for key, value in immdict.items():
        movie_id = key
    usename = current_user.username
    db.session.add(saved_movies(movieid=movie_id, usename=usename))
    db.session.commit()
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


@app.route("/removeIgnored", methods=["GET", "POST"])
def remove_ignored():
    immdict = request.form.to_dict()
    movie_id = list(immdict.values())
    for key, value in immdict.items():
        movie_id = key
    usename = current_user.username

    ignored_movies.query.filter_by(ignoredmovieid=movie_id, usename=usename).delete()
    db.session.commit()

    return redirect(url_for("user_ignored_movies"))


@app.route("/removeSaved", methods=["GET", "POST"])
def remove_saved():
    immdict = request.form.to_dict()
    movie_id = list(immdict.values())
    for key, value in immdict.items():
        movie_id = key
    usename = current_user.username

    saved_movies.query.filter_by(movieid=movie_id, usename=usename).delete()
    db.session.commit()

    return redirect(url_for("user_saved_movies"))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/details/<movie_id>/reviews", methods=["GET", "POST"])
def get_reviews(movie_id):

    review = request.form["review"]

    usename = current_user.username
    db.session.add(
        reviews(
            review=review,
            movie_id=movie_id,
            usename=usename,
        )
    )
    db.session.commit()
    # return render_template("index.html")
    return get_details(movie_id)


def get_reviews_from_db(movie_id):
    reviews_list = [
        r[0]
        for r in db.session.query(reviews.review)
        .filter_by(movie_id=movie_id)
        .distinct()
    ]
    return reviews_list


def update_db_ids_for_user(usename, valid_ids):
    """
    Updates the DB so that only entries for valid_ids exist in it.
    @param usename: the usename of the current user
    @param valid_ids: a set of movie IDs that the DB should update itself
        to reflect
    """
    existing_ids = {
        v.movieid for v in saved_movies.query.filter_by(usesname=usename).all()
    }
    new_ids = valid_ids - existing_ids
    for new_id in new_ids:
        db.session.add(saved_movies(movieid=new_id, usename=usename))
    if len(existing_ids - valid_ids) > 0:
        for movie in saved_movies.query.filter_by(usename=usename).filter(
            saved_movies.movieid.notin_(valid_ids)
        ):
            db.session.delete(movie)
    db.session.commit()


if __name__ == "__main__":
    #     app.run(
    #         # uncomment following 2 lines once ready for deployment to heroku.
    #         host=os.getenv("IP", "0.0.0.0"),
    #         port=int(os.getenv("PORT", 8080)),
    #         debug=True,
    #     )

    app.run(
        # uncomment following 2 lines once ready for deployment to heroku.
        # host=os.getenv("IP", "0.0.0.0"),
        # port=int(os.getenv("PORT", 8080)),
        debug=True,
    )
