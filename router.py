from flask import Flask
from flask_login import LoginManager
from wtforms import Form, TextField, PasswordField, validators, BooleanField
from flask_login import login_user, logout_user, current_user, login_required, UserMixin
from app import db, app,mail  # app will be the app to run the initialization
from model import User, saved_movies, genre_exclusions, ignored_movies
import requests
from flask import render_template, flash, redirect, url_for, request
from form import LoginForm, RegistrationForm,ResetPasswordRequestForm,ResetPasswordForm
import flask
import os
from flask_sqlalchemy import SQLAlchemy
from moviedb import get_detailed_info, get_id, get_movie_info, get_movie_poster, get_movie_trailer
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

#request to reset password.
@app.route("/reset_request",methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm(request.form)
    if form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash("this email is not regisited!")
            return redirect(url_for('reset_request'))
        send_password_reset_email(user)
        flash('please check your email to reset your password!')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',title="reset password",form=form)

#reset password
@app.route("/reset_password/<token>",methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_jwt_token(token)
    if user is None:
        return redirect(url_for('index'))
    form = ResetPasswordForm(request.form)
    if form.validate():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password reset successfully!')
        return redirect(url_for('login'))
    return render_template('reset.html',token=token,form=form)

@app.route("/user", methods=["GET", "POST"])
def user():
    usename = current_user.username
    saved_movies_list_titles = []
    ignored_movies_list_titles = []
    saved_movie_imgs = []
    ignored_movie_imgs = []
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

    for i in saved_movies_list:
        temp1, temp2 = get_movie_info(i)
        saved_movies_list_titles.append(temp2)
        saved_movie_img = get_movie_poster(i)
        saved_movie_imgs.append(saved_movie_img)
        print(saved_movie_img)

    for i in ignored_movies_list:
        temp1, temp2 = get_movie_info(i)
        ignored_movies_list_titles.append(temp2)
        ignored_movie_img = get_movie_poster(i)
        ignored_movie_imgs.append(ignored_movie_img)
        print(ignored_movie_img)

    return render_template(
        "user.html",
        saved_movies_list_titles=saved_movies_list_titles,
        ignored_movies_list_titles=ignored_movies_list_titles,
        saved_movie_imgs=saved_movie_imgs,
        ignored_movie_imgs=ignored_movie_imgs,
    )


@app.route("/details", methods=["GET", "POST"])
def details():
    # this is a very abnormal way to get this data passed, we are kind of exploiting how HTML is structured to pass varriables
    # this scales very poorly, but it works in this case.
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
        trailer_url=trailer_url
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

    #stmt = ignored_movies.delete().where(ignoredmovieid=movie_id).where(usename=usename)
    #db.execute(stmt)

    return redirect(url_for("user"))


@app.route("/removeSaved", methods=["GET", "POST"])
def remove_saved():
    immdict = request.form.to_dict()
    movie_id = list(immdict.values())
    for key, value in immdict.items():
        movie_id = key
    usename = current_user.username

    stmt = saved_movies.query.filter_by(movieid=movie_id).filter_by(usename=usename).delete()
    print("----------------------------------------------")
    print("----------------------------------------------")
    print(stmt)
    print("----------------------------------------------")
    print("----------------------------------------------")
    db.session.execute(stmt)
    db.session.commit()

    return redirect(url_for("user"))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


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
    app.run(
        # uncomment following 2 lines once ready for deployment to heroku.
        #host=os.getenv("IP", "0.0.0.0"),
        #port=int(os.getenv("PORT", 8080)),
        debug=True,
    )
