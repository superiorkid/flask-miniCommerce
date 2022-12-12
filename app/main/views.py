from flask_login import login_required, current_user
from flask import render_template, current_app, request, redirect, url_for, session
from midtransclient import Snap
from datetime import datetime

import os
import requests

from . import main
from ..models import Product, User, Category


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
    data = request.get_json()
    session['cart'] = data

    return redirect(url_for('main.payment'))


@ main.get('/checkout')
@ login_required
def payment():
    if "cart" not in session:
        return redirect(url_for('cart.cart_list'))

    carts = session['cart']
    new_carts = [{
        "id": f'product-{cart.get("name")}-{current_user.id}',
        "price": cart.get('price'),
        "quantity": cart.get('quantity'),
        "name": cart.get('name')
    } for cart in carts]

    snap = Snap(
        is_production=False,
        server_key=current_app.config['SERVER_KEY'],
        client_key=current_app.config['CLIENT_KEY']
    )

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transaction_token = snap.create_transaction_token({
        "transaction_details": {
            "order_id": f"minicommerce-{current_user.id}-{timestamp}",
            "gross_amount": carts[0]["total"]
        }, "credit_card": {
            "secure": True
        }, "item_details": new_carts,
        "customer_details": {
            "first_name": current_user.fname,
            "last_name": current_user.lname,
            "email": current_user.email,
            "phone": f"+{current_user.phone}",
            "billing_address": {
                "first_name": current_user.fname,
                "last_name": current_user.lname,
                "email": current_user.email,
                "phone": f"+{current_user.phone}",
                "address": current_user.address,
                "city": current_user.city,
                "postal_code": current_user.zipcode
            },
            "shipping_address": {
                "first_name": current_user.fname,
                "last_name": current_user.lname,
                "email": current_user.email,
                "phone": f"+{current_user.phone}",
                "address": current_user.address,
                "city": current_user.city,
                "postal_code": current_user.zipcode
            }
        }
    })
    return render_template('cart/checkout.html', carts=carts, token=transaction_token, client_key=snap.api_config.client_key)
