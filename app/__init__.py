"""
App init file
"""

# import Flask module
from flask import Flask, abort, jsonify, request, make_response

# import configurations variables
from instance.config import APP_CONFIG

"""
define create_app to create and return Flask app
"""
def create_app(config_name): # pylint: disable=too-many-locals
    """
    Create our app and return it
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(APP_CONFIG[config_name])
    app.config.from_pyfile("config.py")

    from .auth import AUTH_BLUEPRINT
    app.register_blueprint(AUTH_BLUEPRINT)

    return app
