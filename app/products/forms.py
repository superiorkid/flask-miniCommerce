from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms.widgets import NumberInput
from flask_ckeditor import CKEditorField

from ..models import Product
from ..utility.better_decimal_field import BetterDecimalField


class ProductForm(FlaskForm):
    sku = StringField("Sku", validators=[
                      DataRequired(), Length(1, 50)])
    product_name = StringField("Product Name", validators=[
                               DataRequired(), Length(0, 100)])
    description = CKEditorField("Description", validators=[DataRequired()])
    image = FileField("Choose Image...", validators=[
        FileRequired(), FileAllowed(['png', 'jpg', 'jpeg'], 'png/jpg/jpeg Only!')])
    quantity = StringField("Quantity", validators=[
                           DataRequired()], widget=NumberInput(min=0))
    regular_price = BetterDecimalField('Price', validators=[DataRequired()])
    submit = SubmitField("Add Product")

    def validate_sku(self, field):
        sku = Product.query.filter_by(sku=field.data).first()
        if sku:
            raise ValidationError("Sku is available")


class EditProductForm(ProductForm):
    sku = StringField("Sku", validators=[
                      DataRequired(), Length(1, 50)])
    product_name = StringField("Product Name", validators=[
                               DataRequired(), Length(0, 100)])
    description = CKEditorField("Desctiption", validators=[
                                DataRequired()])
    image = FileField("Choose Image...", validators=[
        FileRequired()])
    quantity = StringField("Quantity", validators=[
                           DataRequired()], widget=NumberInput(min=0))
    regular_price = BetterDecimalField("Price", validators=[DataRequired()])
    submit = SubmitField("Edit Product")
