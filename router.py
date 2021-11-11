from flask import Flask
from flask_login import LoginManager
from wtforms import Form,TextField,PasswordField,validators,BooleanField
from flask_login import login_user, logout_user, current_user, login_required,UserMixin
from app import db,app  #app will be the app to run the initialization
from model import User
import requests
from flask import render_template, flash, redirect, url_for, request
from form import LoginForm, RegistrationForm

login = LoginManager()
login.login_view = "login"
login.init_app(app)



@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
@app.route('/index')
@login_required
def index():
    #main page here
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        if User.query.filter_by(username=form.username.data).first():
            flash ("The user name already exist, please try a new one.")
            return redirect(url_for('register'))
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
	app.run(
        #uncomment following 2 lines once ready for deployment to heroku.
		host=os.getenv('IP', '0.0.0.0'),
		port=int(os.getenv('PORT', 8080)),
		debug=True
	)