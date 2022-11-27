from flask import render_template
from flask_login import login_required

from . import admin
from ..decorators import admin_required


@admin.get('/')
@login_required
@admin_required
def admin():
    return render_template('admin/admin.html')
