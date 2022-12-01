from flask import Blueprint

from ..models import Product

products = Blueprint("products", __name__)

from . import views