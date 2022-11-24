from flask_login import login_required
from flask import redirect, url_for

from . import main


@main.get('/')
@login_required
def index():
    return "show all products user"
