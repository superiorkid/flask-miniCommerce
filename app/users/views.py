import os.path

from flask_login import login_required
from flask import render_template, flash, redirect, url_for, current_app, abort, jsonify
from flask_login import current_user
from datetime import datetime
from werkzeug.utils import secure_filename

import requests

from . import users
from .. import db
from ..decorators import admin_required
from .forms import EditProfileForm, EditProfileAdminForm, ProofOfPaymentForm
from ..models import User, Role, Orders, ProofOfPayment


@users.get('/')
@login_required
@admin_required
def user_list():
    users = User.query.all()
    return render_template('users/user_list.html', users=users)


@users.get('/me')
@login_required
def user_profile():
    user = User.query.filter_by(id=current_user.id).first()
    return render_template('users/profile.html', user=user)


@ users.get('/edit')
@ users.post('/edit')
@ login_required
def edit_profile():
    form = EditProfileForm()
    user = User.query.filter_by(id=current_user.id).first()

    if form.validate_on_submit():
        user.fname = form.fname.data
        user.lname = form.lname.data
        user.address = form.address.data
        user.city = form.city.data
        user.state = form.state.data
        user.country = form.country.data
        user.zipcode = form.zipcode.data
        user.phone = form.phone.data
        user.updated_at = datetime.utcnow()

        db.session.commit()
        flash("User update successfully!!")
        return redirect(url_for('users.user_profile'))

    form.fname.data = user.fname
    form.lname.data = user.lname
    form.address.data = user.address
    form.city.data = user.city
    form.state.data = user.state
    form.country.data = user.country
    form.zipcode.data = user.zipcode
    form.phone.data = user.phone
    return render_template('users/edit_profile.html', form=form, user=user, key=current_app.config['KEY'])


@ users.get('/<int:id>/edit')
@ users.post('/<int:id>/edit')
@ login_required
@ admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user)

    if form.validate_on_submit():
        user.fname = form.fname.data
        user.lname = form.lname.data
        user.address = form.address.data
        user.city = form.city.data
        user.state = form.state.data
        user.country = form.country.data
        user.zipcode = form.zipcode.data
        user.phone = form.phone.data
        user.role = Role.query.get(form.role.data)
        user.updated_at = datetime.utcnow()

        db.session.commit()
        flash("User update successfully!!")
        return redirect(url_for('users.user_list'))

    form.fname.data = user.fname
    form.lname.data = user.lname
    form.address.data = user.address
    form.city.data = user.city
    form.state.data = user.state
    form.country.data = user.country
    form.zipcode.data = user.zipcode
    form.phone.data = user.phone
    form.role.data = user.role_id
    return render_template('users/edit_profile_admin.html', form=form, user=user)


@ users.get('/<int:id>/delete')
@ login_required
@ admin_required
def user_delete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash("User delete successfully.")


@users.get('/get_provinces')
def get_user_province():
    try:
        r = requests.get('https://api.rajaongkir.com/starter/province', headers={
            "key": current_app.config['KEY']
        })
    except requests.exceptions.RequestException as e:
        abort(500)

    provinces = r.json()['rajaongkir']['results']
    return jsonify(provinces)


@users.get('/get_cities/<province_id>')
def get_cities(province_id):
    try:
        r = requests.get(
            f'https://api.rajaongkir.com/starter/city?province={province_id}', headers={
                "key": current_app.config['KEY']
            })
    except requests.exceptions.RequestException as e:
        abort(500)

    cities = r.json()['rajaongkir']['results']
    return jsonify(cities)


@users.get('/transaction-history')
@login_required
def history():
    orders = Orders.query.filter_by(customer_id=current_user.id).all()
    return render_template('users/history.html', orders=orders)


# proof of payment
@users.get('/paying/<int:id>')
@users.post('/paying/<int:id>')
@login_required
def proof_of_payment(id):
    form = ProofOfPaymentForm()
    UPLOAD_DIR = os.path.join(current_app.config['UPLOAD_FOLDER'], "transaction_image")

    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    order = Orders.query.get(id)

    if form.validate_on_submit():
        try:
            payer, date, payment_method, image = form.payer.data,form.date.data, form.payment_method.data, form.image.data
            filename = secure_filename(image.filename)
            pop = ProofOfPayment(date=date, payer=payer, payment_method=payment_method, proof_of_payment=filename, paying=order)
            image.save(os.path.join(UPLOAD_DIR, filename))

            order.status = "capture"

            db.session.add(pop)
            db.session.commit()

            flash("Submit proof of successful payment. please wait for confirmation from the store. thank you!!", "success")
            return redirect(url_for("users.history"))

        except:
            abort(500)


    return render_template("proof_of_pay.html", form=form)


@users.get('/pop_details/<int:id>')
@login_required
@admin_required
def pop_details(id):
    try:
        order = Orders.query.get(id)
        pop_ = order.proof_of_payment
        return render_template('pop_details.html', pop=pop_)
    except:
        abort(500)


@users.get('/<int:id>/accept')
@login_required
@admin_required
def onAccept(id):
    try:
        order = Orders.query.get(id  )
        order.status = "success"
        db.session.commit()
        return redirect(url_for("users.orders"))
    except:
        abort(404)


@users.get('/<int:id>/decline')
@login_required
@admin_required
def onDecline(id):
    try:
        order = Orders.query.get(id)
        order.status = "cancel"
        db.session.commit()
        return redirect(url_for("users.orders"))
    except:
        abort(404)