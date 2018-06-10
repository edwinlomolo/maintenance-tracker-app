"""
Admin views
"""
from flask import request, jsonify
from flask.views import MethodView
from models.db import Db
from models.user import User
from utils.bool import to_bool
from . import ADMIN_BLUEPRINT

DB = Db()

class GetRequest(MethodView):
    """
    Get requests view class
    """
    def get(self):
        """
        Handle get requests on this view
        """
        auth_header = request.headers["Authorization"]
        token = auth_header.split(" ")[1]

        if token:
            user = User.decode_token(token)
            if not isinstance(user, str):
                is_admin = to_bool(user["is_admin"])
                if is_admin:
                    requests = DB.get_all()
                    if requests is not None:
                        return jsonify(requests), 200
                    return jsonify({"message": "Requests not created yet"}), 404
                return jsonify({"message": "You don't have the right access to access this view"}), 401
            return jsonify({"message": str(user)}), 401
        return jsonify({"message": "Something went wrong"}), 500

ADMIN_VIEW = GetRequest.as_view("admin_get_view")
ADMIN_BLUEPRINT.add_url_rule(
    "/api/v1/requests/",
    view_func=ADMIN_VIEW,
    methods=["GET"]
)

class ApproveRequest(MethodView):
    """
    Put request handler for approving request
    """
    def put(self, request_id):
        """
        Handle PUT requests
        """
        if request.json.get('approved'):
            auth_header = request.headers["Authorization"]
            token = auth_header.split(" ")[1]

            if token:
                user = User.decode_token(token)
                is_admin = to_bool(user["is_admin"])
                if is_admin:
                    req = DB.get_request(request_id)
                    obj = {
                        "id": req["id"],
                        "title": req["title"],
                        "description": req["description"],
                        "location": req["location"],
                        "approved": request.json.get('approved'),
                        "rejected": req["rejected"],
                        "resolved": "Pending"
                    }
                    DB.approve_request(request.json.get('approved'), request_id)
                    return jsonify(obj), 200
                return jsonify({
                    "message": "You don't have the right access to approve this request."
                }), 401
            return jsonify({"message": "Something went wrong."}), 500
        return jsonify({"message": "You only need to approve a request."}), 400

APPROVE_VIEW = ApproveRequest.as_view("approve_view")
ADMIN_BLUEPRINT.add_url_rule(
    "/api/v1/requests/<int:request_id>/approve/",
    view_func=APPROVE_VIEW,
    methods=["PUT"]
)

class RejectRequest(MethodView):
    """
    Class for reject view
    """
    def put(self, request_id):
        """
        Handle PUT requests
        """
        if request.json.get('rejected'):
            auth_header = request.headers["Authorization"]
            token = auth_header.split(" ")[1]

            if token:
                user = User.decode_token(token)
                is_admin = to_bool(user["is_admin"])
                if is_admin:
                    req = DB.get_request(request_id)
                    obj = {
                        "id": req["id"],
                        "title": req["title"],
                        "description": req["description"],
                        "location": req["location"],
                        "approved": req["approved"],
                        "rejected": request.json.get('rejected'),
                        "resolved": req["resolved"]
                    }
                    DB.reject_request(request.json.get('rejected'), request_id)
                    return jsonify(obj), 200
                return jsonify({
                    "message": "You don't have the right access to reject this request."
                }), 401
            return jsonify({"message": "Something went wrong."}), 500
        return jsonify({"message": "You only need to reject a request."}), 400

REJECT_VIEW = RejectRequest.as_view("reject_view")
ADMIN_BLUEPRINT.add_url_rule(
    "/api/v1/requests/<int:request_id>/reject/",
    view_func=REJECT_VIEW,
    methods=["PUT"]
)

class ResolveRequest(MethodView):
    """
    Class for reject request view
    """
    def put(self, request_id):
        """
        Handle PUT requests
        """
        if request.json.get('resolved'):
            auth_header = request.headers["Authorization"]
            token = auth_header.split(" ")[1]

            if token:
                user = User.decode_token(token)
                is_admin = to_bool(user["is_admin"])
                if is_admin:
                    req = DB.get_request(request_id)
                    obj = {
                        "id": req["id"],
                        "title": req["title"],
                        "description": req["description"],
                        "location": req["location"],
                        "approved": req["approved"],
                        "rejected": req["rejected"],
                        "resolved": request.json.get('resolved')
                    }
                    DB.resolve_request(request.json.get('resolved'), request_id)
                    return jsonify(obj), 200
                return jsonify({
                    "message": "You don't have the right access to resolve this request."
                }), 401
            return jsonify({"message": "Something went wrong."}), 500
        return jsonify({"message": "You only need to resolve a request."}), 400

RESOLVE_VIEW = ResolveRequest.as_view("resolve_view")
ADMIN_BLUEPRINT.add_url_rule(
    "/api/v1/requests/<int:request_id>/resolve/",
    view_func=RESOLVE_VIEW,
    methods=["PUT"]
)
