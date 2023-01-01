from flask_login import login_required, current_user
from flask import render_template, jsonify, current_app, request, flash, redirect, url_for, session, abort
from datetime import datetime, timedelta

import os
import requests
import json

from .forms import OrdersForm
from . import main
from ..models import Product, User, Category, OrderItem, Orders, Permission
from .. import db
from ..decorators import  permission_required

@main.get('/')
@login_required
def index():
    products = Product.query.all()
    categories = Category.query.all()

    category = request.args.get('category')
    if category:
        cat = Category.query.filter_by(name=category).first()
        filter_by_category = Product.query.filter(
            Product.category.contains(cat)).all()
        return render_template('index.html', filter_by_category=filter_by_category, categories=categories, category=category)

    return render_template('index.html', products=products, categories=categories)


@ main.post('/checkout')
@ login_required
def checkout():
    cart = request.get_json(force=True)
    session['cart'] = cart

    return redirect(url_for('main.payment'))


@ main.get('/pay')
@ main.post('/pay')
def payment():
    # check if cart in session
    if "cart" not in session:
        return redirect(url_for('cart.cart_list'))

    # get data from session
    carts = session['cart']
    form = OrdersForm()

    if form.validate_on_submit():
        penerima, alamat, pesan = form.penerima.data, form.alamat.data, form.pesan.data
        new_order = Orders(customer_id=current_user.id, penerima=penerima, alamat=alamat, pesan=pesan, total=carts['total'])

        for cart in carts['detail']:
            product = Product.query.filter_by(product_name=cart['name']).first()
            new_order_item = OrderItem(quantity=cart['quantity'], price=cart['cost'], product_id=product.id)
            db.session.add(new_order_item)
            new_order.items.append(new_order_item)

            # reduce the product quantity every time pay is clicked
            product.quantity -= int(cart["quantity"])

        # delete user cart
        user = User.query.get(current_user.id)
        user.products.clear()

        db.session.add(user)
        db.session.add(new_order)
        db.session.commit()
        flash('Order has been made. Please pay!!', 'success')
        return redirect(url_for('users.history'))

    return render_template('cart/checkout.html', carts=carts, form=form)


@main.before_request
def before_request_fucn():
    orders = Orders.query.all()

    if orders:
        for order in orders:
            if order.status == "pending":
                more_than_one_day = datetime.today() - timedelta(days=1)
                if order.created_at < more_than_one_day:
                    order.status = "expired"
                    db.session.commit()


@main.get('/invoice/<int:id>')
@login_required
def invoice(id):
    order = Orders.query.get(id)
    return render_template('invoice.html', order=order)

@main.get('/orders')
@login_required
@permission_required(Permission.PRODUCT_MANAGEMENT)
def orders():
    orders = Orders.query.all()
    return render_template("orders.html", orders=orders)


@main.get('/cancel_order/<int:id>')
@login_required
def cancel_order(id):
    try:
        order = Orders.query.get(id)
        items = OrderItem.query.filter_by(orders=order).all()

        for item in items:
            # returns the quantity of products that are canceled in the order.
            item.product.quantity += item.quantity
            db.session.add(item)

        order.status = "cancel"
        db.session.commit()
        return redirect(url_for('users.history'))
    except:
        abort(500)
