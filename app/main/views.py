from flask_login import login_required, current_user
from flask import render_template, jsonify, current_app, request, flash, redirect, url_for, session
from datetime import datetime


import os
import requests
import json

from .forms import OrdersForm
from . import main
from ..models import Product, User, Category, OrderItem, Orders
from .. import db


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
        new_order = Orders(customer_id=current_user.id, penerima=penerima,
                           alamat=alamat, pesan=pesan, total=carts['total'])

        for cart in carts['detail']:
            product = Product.query.filter_by(
                product_name=cart['name']).first()
            new_order_item = OrderItem(
                quantity=cart['quantity'], price=cart['cost'], items=product)
            db.session.add(new_order_item)
            new_order.items.append(new_order_item)

        db.session.add(new_order)
        db.session.commit()
        flash('Success', 'success')
        return redirect(url_for('main.index'))

    return render_template('cart/checkout.html', carts=carts, form=form)
