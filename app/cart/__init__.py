from flask import Blueprint
from flask_login import current_user

cart = Blueprint("cart", __name__)

from . import views

@cart.app_context_processor
def inject_cart_total():
    if current_user.is_anonymous:
        return dict(TotalCart=0)

    return dict(TotalCart=len(current_user.products))


