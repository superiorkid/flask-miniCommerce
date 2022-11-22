from flask import render_template
from flask_login import login_required
from ..decorators import admin_required

from . import main


@main.get("/")
@login_required
def index():
    return render_template("index.html", page="index")


@main.get('/admin')
@login_required
@admin_required
def admin_page():
    return render_template('admin.html', page="admin")
