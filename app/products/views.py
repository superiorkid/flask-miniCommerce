
from flask import request, render_template, current_app, flash, redirect, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename

import os

from .. import db
from ..decorators import permission_required
from . import products
from ..models import Permission, Product
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

    if form.validate_on_submit():
        f = form.image.data
        filename = secure_filename(f.filename)

        new_product = Product(sku=form.sku.data, product_name=form.product_name.data, description=form.description.data,
                              image=filename, quantity=form.quantity.data, regural_price=form.regular_price.data)

        if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
            os.makedirs(current_app.config['UPLOAD_FOLDER'])

        f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        db.session.add(new_product)
        db.session.commit()
        flash("New Product has been added")

        return redirect(url_for('products.show_product'))

    return render_template('products/add_product.html', form=form)


@products.get('/<int:id>/detail')
@login_required
@permission_required(Permission.PRODUCT_MANAGEMENT)
def detail_product(id):
    return render_template('product/detail_product.html')


@products.get('/<int:id>/edit')
@products.post('/<int:id>/edit')
@login_required
@permission_required(Permission.PRODUCT_MANAGEMENT)
def edit_product(id):
    form = EditProductForm()

    if form.validate_on_submit():
        pass

    return render_template('products/edit_product.html', form=form)


@products.get('/<int:id>/delete')
@login_required
@permission_required(Permission.PRODUCT_MANAGEMENT)
def delete_product(id):
    product = db.get_or_404(Product, id)
    db.session.delete(product)
    db.session.commit()
    flash("Product delete successfully.")
    return redirect(url_for('products.show_product'))
