from flask import Blueprint
from ..models import Permission

auth = Blueprint('auth', __name__)

from . import views

@auth.app_context_processor
def inject_permissions():
  return dict(Permission=Permission)