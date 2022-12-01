from flask_login import login_required
from flask import render_template

from . import main
from ..models import Product


@main.get('/')
@login_required
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)
