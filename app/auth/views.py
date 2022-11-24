from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import login_user, current_user, login_required, logout_user
from ..email import send_mail

from . import auth
from .forms import LoginForm, RegisterForm
from ..models import User
from .. import db


@auth.get("/signin")
@auth.post("/signin")
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.verify_password(form.password.data):
                login_user(user, form.remember_me.data)
                return redirect(request.args.get("next") or url_for("main.index"))

            flash(
                "The email or password you entered is incorrect, please try again", "error")
        except:
            abort(500)

    return render_template("auth/signin.html", title="Login Form", form=form, page="signin")


@auth.get('/signup')
@auth.post('/signup')
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegisterForm()

    if form.validate_on_submit():
        try:
            user = User(email=form.email.data, password=form.password.data,
                        fname=form.fname.data, lname=form.lname.data)

            db.session.add(user)
            db.session.commit()

            token = user.generate_confirmation_token()
            send_mail(user.email, "Confirmation Your Account!",
                      'auth/email/confirm', token=token)
            flash("A confirmation email has been sent to you by email.")
            return redirect(url_for('main.index'))
        except:
            abort(500)

    return render_template('auth/signup.html', form=form, page="signup")


@auth.get("/logout")
@login_required
def signout():
    logout_user()
    flash("Successfully user logout")
    return redirect(url_for('main.index'))


@auth.get('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))

    if current_user.confirm(token):
        flash("You have confirmed your account. Thanks!")
    else:
        flash('The confirmation link is invalid or has expired.')

    return redirect(url_for('main.index'))
