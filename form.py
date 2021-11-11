<<<<<<< HEAD
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from model import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    # password2 = PasswordField(
    #     'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")
=======
from wtforms import StringField, PasswordField, BooleanField,validators,Form




class LoginForm(Form):
    username = StringField('username', [validators.DataRequired()])
    password = PasswordField('password', [validators.DataRequired()])
    remember_me = BooleanField('remember Me',default = False)

class RegistrationForm(Form):
    username = StringField('username', [validators.DataRequired()])
    password = PasswordField('password', [validators.DataRequired()])


>>>>>>> main
