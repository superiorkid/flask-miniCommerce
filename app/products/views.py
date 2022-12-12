
from flask import request, render_template, current_app, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

import os

from .. import db
from ..decorators import permission_required
from . import products
from ..models import Permission, Product, User, Category
from .forms import ProductForm, EditProductForm


@products.get('/')
@login_required
@permission_required(Permission.PRODUCT_MANAGEMENT)
def show_product():
    products = Product.query.all()
    return render_template('products/product.html', products=products)


@products.post('/add')
@products.get('/add')
@login_required
@permission_required(Permission.PRODUCT_MANAGEMENT)
def insert_product():
    form = ProductForm()
    UPLOAD_DIR = current_app.config['UPLOAD_FOLDER']

    if form.validate_on_submit():
        f = form.image.data
        filename = f"product-img-{form.sku.data}-{f.filename}"
        new_filename = secure_filename(filename)

        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)

        f.save(os.path.join(
            current_app.config['UPLOAD_FOLDER'], new_filename))

        categories = form.category.data.split(',')
        products_category = []
        for category in categories:
            categorys = category.strip()
            products_category.append(categorys)
            if not Category.query.filter_by(name=categorys).first():
                new_category = Category(name=categorys)
                db.session.add(new_category)

            continue

        new_product = Product(sku=form.sku.data, product_name=form.product_name.data, description=form.description.data,
                              image=new_filename, quantity=form.quantity.data, regural_price=form.regular_price.data)

        for pc in products_category:
            ct = Category.query.filter_by(name=pc).first()
            new_product.category.append(ct)

            db.session.add(new_product)

        db.session.commit()
        flash("New Product has been added")

        return redirect(url_for('products.show_product'))

    return render_template('products/add_product.html', form=form)


@products.get('/<int:id>/edit')
@products.post('/<int:id>/edit')
@login_required
@permission_required(Permission.PRODUCT_MANAGEMENT)
def edit_product(id):
    UPLOAD_DIR = current_app.config['UPLOAD_FOLDER']
    form = EditProductForm()
    products = db.get_or_404(Product, id)

    if form.validate_on_submit():
        if form.image.data:
            f = form.image.data
            head, tail = os.path.split(f.filename)
            new_filename = secure_filename(
                f"product-img-{form.sku.data}-{tail}")

            if not os.path.exists(UPLOAD_DIR):
                os.makedirs(UPLOAD_DIR)

            f.save(os.path.join(UPLOAD_DIR, new_filename))

            products.image = new_filename

        products.sku = form.sku.data
        products.product_name = form.product_name.data
        products.description = form.description.data
        products.quantity = form.quantity.data
        products.regural_price = form.regular_price.data

        db.session.commit()
        flash("Product update successfully")
        return redirect(url_for('products.show_product'))

    form.sku.data = products.sku
    form.product_name.data = products.product_name
    form.description.data = products.description
    form.quantity.data = products.quantity
    form.regular_price.data = products.regural_price
    form.image.data = products.image

    image_path = os.path.join(UPLOAD_DIR, products.image)
    return render_template('products/edit_product.html', form=form, products=products, image_path=image_path)


@products.get('/<int:id>/detail')
@login_required
def detail_product(id):
    product = db.get_or_404(Product, id)
    all_product = Product.query.all()
    return render_template('products/detail_product.html', product=product, all_product=all_product)


@products.get('/<int:id>/delete')
@login_required
@permission_required(Permission.PRODUCT_MANAGEMENT)
def delete_product(id):
    UPLOAD_DIR = current_app.config['UPLOAD_FOLDER']
    product = db.get_or_404(Product, id)

    path = os.path.join(UPLOAD_DIR, product.image)
    if os.path.exists(path):
        os.remove(path)

    db.session.delete(product)
    db.session.commit()
    flash("Product delete successfully.")
    return redirect(url_for('products.show_product'))
