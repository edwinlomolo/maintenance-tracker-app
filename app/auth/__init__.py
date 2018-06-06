"""
Authentication Blueprint
"""
from flask import Blueprint
from . import views

# instance of blueprint that instantiate authentication blueprint
AUTH_BLUEPRINT = Blueprint("auth", __name__)
