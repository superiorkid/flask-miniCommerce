from flask import render_template, redirect, url_for
from flask_login import current_user, login_required

from . import main


@main.get("/")
@login_required
def index():
    return render_template("index.html")
