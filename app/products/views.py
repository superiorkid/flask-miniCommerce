from . import products

from flask import request
from flask_login import login_required
from ..decorators import admin_required


@products.get('/')
@products.post('/')
@login_required
@admin_required
def show_product():
    if request.method == "GET":
        return "Show all products"

    if request.method == "POST":
        return "inserted product"


@products.get('/<id>/detail')
def detail_product(id):
    return "show product by id"


@products.post('/<id>/update')
def update_product(id):
    return "update products"


@products.get('/<id>/delete')
def delete_product(id):
    return "delete product"
