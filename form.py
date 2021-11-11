from wtforms import StringField, PasswordField, BooleanField, validators, Form


class LoginForm(Form):
    username = StringField("username", [validators.DataRequired()])
    password = PasswordField("password", [validators.DataRequired()])
    remember_me = BooleanField("remember Me", default=False)


class RegistrationForm(Form):
    username = StringField("username", [validators.DataRequired()])
    password = PasswordField("password", [validators.DataRequired()])
