from flask_login import login_required
from flask import render_template, flash, redirect, url_for
from flask_login import current_user

from . import users
from .. import db
from ..decorators import admin_required
from .forms import EditProfileForm, EditProfileAdminForm
from ..models import User, Role


@users.get('/')
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
    return render_template('users/edit_profile.html', form=form, user=user)


@users.get('/list')
@login_required
@admin_required
def user_list():
    users = User.query.all()
    return render_template('users/user_list.html', users=users)


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
