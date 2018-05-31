# import Flask module
from flask import Flask, abort, jsonify, request, make_response

# import configurations variables
from instance.config import app_config

# define create_app to create and return Flask app
def create_app(config_name):

	from models.user import User
	from models.request import Request

	app = Flask(__name__, instance_relative_config=True)
	app.config.from_object(app_config[config_name])
	app.config.from_pyfile("config.py")

	requests = [
		{
			"id": 1,
			"title": "Bad weather road",
			"description": "Too many potholes. Gets muddy when it rains",
			"location": "Kitui",
			"created_by": "Mike",
			"approved": False,
			"rejected": True,
			"resolved": True
		}
	]
	accounts = [
		{
			"firstname": "Milly",
			"lastname": "Doe",
			"email": "milly@gmail.com",
			"password": 4747
		}
	]
	
	# user post request route
	@app.route("/users/api/v1.0/requests/", methods=["POST"])
	def create_request():
		id = requests[-1]["id"] + 1
		title = request.json.get('title')
		description = request.json.get('description')
		location = request.json.get('location')
		created_by = request.json.get('created_by')
		if request.json:
			req = Request(id=id, title=title, description=description, location=location, created_by=created_by)
			requests.append(req)
			return jsonify({
				"id": req.id,
				"title": req.title,
				"description": req.description,
				"location": req.location,
				"created_by": req.created_by,
				"approved": req.approved,
				"rejected": req.rejected,
				"resolved": req.resolved
			}), 201

	# user account registration view
	@app.route("/users/api/v1.0/account/register/", methods=["POST"])
	def create_account():
		if request.json:

			firstname = request.json.get('firstname')
			lastname = request.json.get('lastname')
			email = request.json.get('email')
			password = request.json.get('password')

			user = User(firstname=firstname, lastname=lastname, email=email, password=password)
			accounts.append(user)
			return jsonify({
				"message": "Your account was created successfully."
			}), 201

	# user login view
	@app.route("/users/api/v1.0/authenticate/", methods=["POST"])
	def login_user():
		if request.json:
			email = request.json.get('email')
			password = request.json.get('password')

			for account in accounts:
				if account["email"] == email:
					if account["password"] == password:
						return jsonify({
							"status": "Success",
							"message": "Login was successfull",
							"email": account["email"]
						}), 200
					return jsonify({
						"message": "Invalid password"
					}), 401
			abort(404)

	# get all requests view
	@app.route("/users/api/v1.0/requests/", methods=["GET"])
	def get_requests():
		name = request.headers["role"]
		reqs = []
		for item in requests:
			if item["created_by"] == name:
				req = {
					"id": item["id"],
					"title": item["title"],
					"description": item["description"],
					"location": item["location"],
					"approved": item["approved"],
					"rejected": item["rejected"],
					"resolved": item["resolved"],
					"created_by": item["created_by"]
				}
				reqs.append(req)
		return jsonify(reqs), 200

	# get a request view
	@app.route("/users/api/v1.0/requests/<int:id>/", methods=["GET"])
	def get_request(id):
		name = request.headers["role"]
		reqs = []
		for item in requests:
			if item["created_by"] == name:
				if item["id"] == id:
					req = {
						"id": item["id"],
						"title": item["title"],
						"description": item["description"],
						"location": item["location"],
						"approved": item["approved"],
						"rejected": item["rejected"],
						"resolved": item["resolved"],
						"created_by": item["created_by"]
					}
					reqs.append(req)
		return jsonify(reqs), 200

	# update request view
	@app.route("/users/api/v1.0/requests/<int:id>/", methods=["PUT"])
	def update_request(id):
		if request.json:
			req = [item for item in requests if item["id"] == id]

			req[0]["title"] = request.json.get('title', req[0]["title"])
			req[0]["description"] = request.json.get('description', req[0]["description"])
			req[0]["location"] = request.json.get('location', req[0]["location"])
			req[0]["created_by"] = request.json.get('created_by', req[0]["created_by"])

			return jsonify({
				"id": req[0]["id"],
				"title": req[0]["title"],
				"description": req[0]["description"],
				"location": req[0]['location'],
				"created_by": req[0]["created_by"],
				"approved": req[0]["approved"],
				"rejected": req[0]["rejected"],
				"resolved": req[0]["resolved"]
			}), 200

	# get requests for admin
	@app.route("/admin/api/v1.0/requests/", methods=["GET"])
	def get_requests_for_admin():
		role = str(request.headers["role"])
		if role == "admin":
			return jsonify(requests), 200

	# put request for admin
	@app.route("/admin/api/v1.0/requests/<int:id>/", methods=["PUT"])
	def update(id):
		role = str(request.headers["role"])
		req = [item for item in requests if item["id"] == id]

		req[0]["approved"] = request.json.get('approved', req[0]["approved"])
		req[0]["rejected"] = request.json.get('rejected', req[0]["rejected"])
		req[0]["resolved"] = request.json.get('resolved', req[0]["resolved"])

		return jsonify({
			"id": req[0]["id"],
			"title": req[0]["title"],
			"description": req[0]["description"],
			"location": req[0]["location"],
			"approved": req[0]["approved"],
			"rejected": req[0]["rejected"],
			"resolved": req[0]["resolved"]
		}), 200

	# get request for admin
	@app.route("/admin/api/v1.0/requests/<int:id>/", methods=["GET"])
	def get_single_request(id):
		role = request.headers["role"]
		if id > len(requests):
			abort(404)
		if role == "admin":
			req = [item for item in requests if item["id"] == id]

			return jsonify({
				"id": req[0]["id"],
				"title": req[0]["title"],
				"description": req[0]["description"],
				"location": req[0]["location"],
				"approved": req[0]["approved"],
				"rejected": req[0]["rejected"],
				"resolved": req[0]["resolved"]
			}), 200

	@app.errorhandler(404)
	def not_found(error):
		return make_response(jsonify({ "error": "Not Found"})), 404

	return app
