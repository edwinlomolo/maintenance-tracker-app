"""
App init file
"""

# import Flask module
from flask import Flask, abort, jsonify, request, make_response

# import configurations variables
from instance.config import APP_CONFIG

# Get DB
from models.db import Db

# Get utils
from utils.bool import to_bool

DB = Db()

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

    @app.route("/api/v1/users/requests/", methods=["POST"])
    def create_request():
        """
        Create new request for logged in user
        """
        auth_header = request.headers["Authorization"] # get authorization header
        token = auth_header.split(" ")[1] # split header to obtain token

        if token:
            user = User.decode_token(token)
            # check if user is a string
            if not isinstance(user, str):
                if request.json and request.json.get('title') and \
                request.json.get('description') and request.json.get('location'):
                    title = request.json.get('title')
                    description = request.json.get('description')
                    location = request.json.get('location')
                    req = Request(
                        title=title,
                        description=description,
                        location=location,
                        created_by=user["id"]
                    )
                    req.save()
                    return make_response(jsonify({
                        "title": req.title,
                        "description": req.description,
                        "location": req.location,
                        "created_by": req.created_by
                    })), 201
                return make_response(jsonify({
                    "error": "Please provide the title, description, and location of you request."
                })), 400
            return make_response(jsonify({"message": str(user)})), 401
        return make_response(jsonify({"message": "Invalid request"})), 500

    @app.route("/api/v1/users/requests/", methods=["GET"])
    def get_requests():
        """
        Get all requests for a logged in user
        """

        auth_header = request.headers["Authorization"] # Get Authorization value
        token = auth_header.split(" ")[1] # split auth_header to access token value at position 1

        if token:
            user = User.decode_token(token)
            if not isinstance(user, str):
                result = DB.get_request_by_user_id(user["id"])
                if result is not None:
                    return make_response(jsonify(result)), 200
                return make_response(jsonify({"message": "No requests created by you currently. Create to view."})), 404
            return make_response(jsonify({"message": str(user)})), 401
        return make_response(jsonify({"message": "Something went wrong."})), 500

    @app.route("/api/v1/users/requests/<int:request_id>/", methods=["GET"])
    def get_request(request_id):
        """
        Get a request for a logged in user
        """
        auth_header = request.headers["Authorization"] # get Authorization value
        token = auth_header.split(" ")[1] # get user token

        if token:
            user = User.decode_token(token)
            if not isinstance(user, str):
                result = DB.get_request_by_id(request_id, user["id"])
                if result is not None:
                    return make_response(jsonify(result)), 200
                return make_response(jsonify({"message": "You have no request of id {} created by you.".format(request_id)})), 401
            return make_response(jsonify({"message": str(user)})), 401
        return make_response(jsonify({"message": "Something went wrong"})), 500

    @app.route("/api/v1/users/requests/<int:request_id>/", methods=["PUT"])
    def edit_request(request_id):
        """
        Logged in user can edit his/her request
        """
        if request.json:
            auth_header = request.headers["Authorization"]
            token = auth_header.split(" ")[1]

            user = User.decode_token(token)
            if not isinstance(user, str):
                result = DB.get_request_by_id(request_id, user["id"])
                if result is not None:
                    if result["resolved"] == "Pending":
                        return make_response(jsonify({
                            "message": "This request is already approved. You can't revert, instead create a new one."
                        })), 401
                    obj = {
                        "title": request.json.get('title', result["title"]),
                        "description": request.json.get('description', result["description"]),
                        "location": request.json.get('location', result["location"]),
                        "approved": result["approved"],
                        "rejected": result["rejected"],
                        "resolved": result["resolved"]
                    }
                    DB.update_request(obj["title"], obj["description"],
                                      obj["location"], obj["approved"], obj["rejected"],
                                      obj["resolved"], request_id, user["id"])
                    return make_response(jsonify(obj)), 200
                return make_response(jsonify({"message": "Can't find request {} created by you. You may not have the right access to that request.".format(request_id)})), 401
            return make_response(jsonify({"message": str(user)})), 401
        return make_response(jsonify({"message": "You only have the right access to edit your request title, description and location"})), 400

    from .auth import AUTH_BLUEPRINT
    app.register_blueprint(AUTH_BLUEPRINT)

    from .admin import ADMIN_BLUEPRINT
    app.register_blueprint(ADMIN_BLUEPRINT)

    return app
