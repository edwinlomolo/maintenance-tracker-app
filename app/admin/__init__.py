"""
Admin Blueprint
"""
from flask import Blueprint

# Instance of Blueprint that instantiate Admin Blueprint
ADMIN_BLUEPRINT = Blueprint("admin", __name__)

from . import views # pylint: disable=wrong-import-position
