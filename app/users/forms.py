from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Length, ValidationError
from flask import abort, current_app

import requests
import phonenumbers

from ..models import User, Role


class EditProfileForm(FlaskForm):
    fname = StringField("First Name", validators=[Length(
        0, 30)], render_kw={"placeholder": "First Name"})
    lname = StringField("Last Name", validators=[Length(
        0, 30)], render_kw={"placeholder": "Last Name"})
    address = StringField('Address', validators=[Length(
        0, 30)], render_kw={"placeholder": "Address"})
    # state = StringField('State', validators=[Length(
    #     0, 30)], render_kw={"placeholder": "State"})
    state = SelectField("State", coerce=str)
    city = SelectField('City', coerce=str)
    country = StringField('Country', validators=[Length(
        0, 30)], render_kw={"placeholder": "Country"})
    zipcode = StringField('Zip Code', validators=[Length(
        0, 30)], render_kw={"placeholder": "Zip Code"})
    phone = StringField('Phone Number', validators=[
                        Length(0, 20)], render_kw={"placeholder": "Phone"})
    submit = SubmitField("Edit")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state.choices = [('0', "--Select State--")] + [(prov['province'],
                                                             prov['province']) for prov in self.get_province()]
        self.city.choices = [("0", "-- Select City --")] + \
            [(city['city_name'], city['city_name'])
             for city in self.get_cities()]

    def get_province(self):
        try:
            r = requests.get('https://api.rajaongkir.com/starter/province', headers={
                "key": current_app.config['KEY']
            })
        except requests.exceptions.RequestException as e:
            abort(500)

        province_list = r.json()['rajaongkir'].get('results')
        return province_list

    def get_cities(self):
        try:
            r = requests.get('https://api.rajaongkir.com/starter/city', headers={
                "key": current_app.config['KEY']
            })
        except requests.exceptions.RequestException as e:
            abort(500)

        cities = r.json()['rajaongkir'].get('results')
        return cities

    def validate_phone(self, field):
        try:
            p = phonenumbers.parse(f"+{field.data}")
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError("Invalid Phone Number.")


class EditProfileAdminForm(FlaskForm):
    fname = StringField("First Name", validators=[Length(
        0, 30)], render_kw={"placeholder": "First Name"})
    lname = StringField("Last Name", validators=[Length(
        0, 30)], render_kw={"placeholder": "Last Name"})
    address = StringField('Address', validators=[Length(
        0, 30)], render_kw={"placeholder": "Address"})
    state = SelectField('State', coerce=str)
    city = SelectField('City', coerce=str)
    country = StringField('Country', validators=[Length(
        0, 30)], render_kw={"placeholder": "Country"})
    zipcode = StringField('Zip Code', validators=[Length(
        0, 30)], render_kw={"placeholder": "Zip Code"})
    phone = StringField('Phone Number', validators=[
                        Length(0, 20)], render_kw={"placeholder": "Phone"})
    role = SelectField("Role", coerce=int)
    submit = SubmitField("Edit")

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.role.choices = [(0, "-- Select Role --")] + [(role.id, role.name)
                                                          for role in Role.query.order_by(Role.name).all()]
        self.state.choices = [('0', "-- Select State --")] + \
            [(prov['province'], prov['province'])
             for prov in self.get_province()]
        self.city.choices = [("0", "-- Select City --")] + \
            [(city['city_name'], city['city_name'])
             for city in self.get_cities()]

    def get_province(self):
        try:
            r = requests.get('https://api.rajaongkir.com/starter/province', headers={
                "key": current_app.config['KEY']
            })
        except requests.exceptions.RequestException as e:
            abort(500)

        province_list = r.json()['rajaongkir'].get('results')
        return province_list

    def get_cities(self):
        try:
            r = requests.get('https://api.rajaongkir.com/starter/city', headers={
                "key": current_app.config['KEY']
            })
        except requests.exceptions.RequestException as e:
            abort(500)

        cities = r.json()['rajaongkir'].get('results')
        return cities

    def validate_phone(self, field):
        try:
            p = phonenumbers.parse(f"+{field.data}")
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError("Invalid Phone Number.")
