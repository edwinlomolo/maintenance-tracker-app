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

    # import Request model
    from models.request import Request
    from models.user import User

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(APP_CONFIG[config_name])
    app.config.from_pyfile("config.py")

    @app.route("/api/v1.0/users/requests/", methods=["POST"])
    def create_request():
        """
        Create new request for logged in user
        """
        auth_header = request.headers["Authorization"] # get authorization header
        token = auth_header.split(" ")[1] # split header to obtain token

        if token:
            user_id = User.decode_token(token)
            # check if user_id is a string
            if not isinstance(user_id, str):
                if request.json and request.json.get('title') and request.json.get('description') and request.json.get('location'):
                    title = request.json.get('title')
                    description = request.json.get('description')
                    location = request.json.get('location')
                    req = Request(
                        title=title,
                        description=description,
                        location=location,
                        created_by=user_id
                    )
                    req.save()
                    return make_response(jsonify({
                        "title": req.title,
                        "description": req.description,
                        "location": req.location,
                        "created_by": req.created_by
                    })), 201
                return make_response(jsonify({
                    "error": "Provide necessary data for making a request."
                })), 400
            return make_response(jsonify({"message": str(user_id)})), 401
        return make_response(jsonify({"message": "Invalid request"})), 500

    @app.route("/api/v1.0/users/requests/", methods=["GET"])
    def get_requests():
        """
        Get all requests for a logged in user
        """

        auth_header = request.headers["Authorization"] # Get Authorization value
        token = auth_header.split(" ")[1] # split auth_header to access token value at position 1

        if token:
            user_id = User.decode_token(token)
            if not isinstance(user_id, str):
                row = User.query(user_id)
                return jsonify(row)

    from .auth import AUTH_BLUEPRINT
    app.register_blueprint(AUTH_BLUEPRINT)

    return app
