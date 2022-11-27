from flask_login import login_required
from flask import render_template

from . import main


@main.get('/')
@login_required
def index():
    return render_template('index.html')
