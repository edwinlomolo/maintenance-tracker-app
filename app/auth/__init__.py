"""
Authentication Blueprint
"""
from flask import Blueprint

# instance of blueprint that instantiate authentication blueprint
AUTH_BLUEPRINT = Blueprint("auth", __name__)

from . import views # pylint: disable=wrong-import-position
