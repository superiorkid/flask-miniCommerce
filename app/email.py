from flask_mail import Message
from dotenv import load_dotenv
from flask import render_template
import os

from . import mail

load_dotenv()


def send_mail(to, subject, template, **kwargs):
    msg = Message(subject, recipients=[
                  to], sender="Admin Flask-miniCommerce")
    # msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)
