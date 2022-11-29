from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Length, ValidationError

import phonenumbers

from ..models import User, Role


class EditProfileForm(FlaskForm):
    fname = StringField("First Name", validators=[Length(
        0, 30)], render_kw={"placeholder": "First Name"})
    lname = StringField("Last Name", validators=[Length(
        0, 30)], render_kw={"placeholder": "Last Name"})
    address = StringField('Address', validators=[Length(
        0, 30)], render_kw={"placeholder": "Address"})
    city = StringField('City', validators=[Length(
        0, 30)], render_kw={"placeholder": "City"})
    state = StringField('State', validators=[Length(
        0, 30)], render_kw={"placeholder": "State"})
    country = StringField('Country', validators=[Length(
        0, 30)], render_kw={"placeholder": "Country"})
    zipcode = StringField('Zip Code', validators=[Length(
        0, 30)], render_kw={"placeholder": "Zip Code"})
    phone = StringField('Phone Number', validators=[
                        Length(0, 20)], render_kw={"placeholder": "Phone"})
    submit = SubmitField("Edit")

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
    city = StringField('City', validators=[Length(
        0, 30)], render_kw={"placeholder": "City"})
    state = StringField('State', validators=[Length(
        0, 30)], render_kw={"placeholder": "State"})
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

    def validate_phone(self, field):
        try:
            p = phonenumbers.parse(f"+{field.data}")
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError("Invalid Phone Number.")
