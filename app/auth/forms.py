from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp, ValidationError

from app.models import User


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[
                        DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField("Password", validators=[
                             DataRequired()], render_kw={"placeholder": "Password"})
    remember_me = BooleanField("Keep me signed in")
    submit = SubmitField("Sign In")


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()], render_kw={
                        "placeholder": "Email"})
    username = StringField("Username", validators=[Regexp(
        '^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers, dots or underscores'), DataRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField("Pasword", validators=[DataRequired(), EqualTo(
        "confirm_password", "Password must match.")], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField("Confirm Password", render_kw={
                                     "placeholder": "Confirm Password"})
    submit = SubmitField("Simpan")

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("Email already registered.")

    def validate_username(self, username):
        username = User.query.filter_by(username=username.data).first()
        if username:
            raise ValidationError("Username already registered.")
