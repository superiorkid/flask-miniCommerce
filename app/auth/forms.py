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
    password = PasswordField("Pasword", validators=[DataRequired(), EqualTo(
        "confirm_password", "Password must match.")], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField("Confirm Password", render_kw={
                                     "placeholder": "Confirm Password"})
    fname = StringField("First Name", validators=[DataRequired()], render_kw={
                        "placeholder": "First Name"})
    lname = StringField('Last Name', validators=[DataRequired()], render_kw={
                        "placeholder": "Last Name"})

    submit = SubmitField("Confirm")

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("Email already registered.")
