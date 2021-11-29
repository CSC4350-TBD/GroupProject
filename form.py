from wtforms import StringField, PasswordField, BooleanField, validators, Form,SubmitField
from wtforms.validators import EqualTo,DataRequired,Email 


class LoginForm(Form):
    username = StringField("username", [validators.DataRequired()])
    password = PasswordField("password", [validators.DataRequired()])
    remember_me = BooleanField("remember Me", default=False)


class RegistrationForm(Form):
    username = StringField("username", [validators.DataRequired()])
    email = StringField("email",validators=[DataRequired(),Email()])
    password = PasswordField("password", [validators.DataRequired()])


class ResetPasswordRequestForm(Form):
    email = StringField("email",validators=[DataRequired(),Email()])

class ResetPasswordForm(Form):
    password = PasswordField("password", [validators.DataRequired()])
    password2 = PasswordField('confirm password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Reset password')

