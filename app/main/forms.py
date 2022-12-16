from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class OrdersForm(FlaskForm):
    penerima = StringField("Recipient's Name", validators=[DataRequired()], render_kw={
                           "placeholder": "Recipient's Name..."})
    alamat = StringField('Recipient Address', validators=[DataRequired()], render_kw={
                         "placeholder": "Recipient Address..."})
    pesan = TextAreaField('Message', render_kw={
                          "placeholder": "leave a message..."})
    submit = SubmitField('Pay!!')
