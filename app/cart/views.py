from flask import flash, jsonify, render_template, redirect, request
from flask_login import current_user, login_required

from . import cart
from ..models import User, Product, Category
from .. import db


@cart.get('/')
@login_required
def cart_list():
    carts = current_user.products
    return render_template('cart/cart.html', carts=carts)


@cart.post("/<int:product_id>/add")
@login_required
def add_to_cart(product_id):
    cart_item = Product.query.filter_by(id=product_id).first()
    user = User.query.filter_by(id=current_user.id).first()

    user.products.append(cart_item)
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "message": "product successfully added to cart."
    })


@cart.delete('/<int:product_id>/remove')
@login_required
def remove_from_cart(product_id):
    cart_item = Product.query.filter_by(id=product_id).first()
    user = User.query.filter_by(id=current_user.id).first()

    user.products.remove(cart_item)
    db.session.commit()
    return jsonify({
        "message": "Product remove from cart"
    })
