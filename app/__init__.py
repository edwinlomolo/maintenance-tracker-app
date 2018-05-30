# import Flask module
from flask import Flask, abort, jsonify, request

# import configurations variables
from instance.config import app_config

# define create_app to create and return Flask app
def create_app(config_name):
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_object(app_config[config_name])
	app.config.from_pyfile("config.py")

	# requests list
	requests = [
		{
			"id": 1,
			"title": "Leaking pipe",
			"description": "I have a busted water pipe in my bathroom. Its has been leaking for a week",
			"location": "Kisumu",
			"approved": False,
			"rejected": False,
			"resolved": False,
			"created_by": "Edwin"
		},
		{
			"id": 2,
			"title": "Security",
			"description": "Crime rate has increased due to tampered security lights.",
			"location": "Bungoma",
			"approved": False,
			"rejected": False,
			"resolved": False,
			"created_by": "Edwin"
		},
		{
			"id": 3,
			"title": "Air pollution",
			"description": "We have a bad smell in the middle of the town coming from garbage collection tanker.",
			"location": "Dandora",
			"approved": False,
			"rejected": False,
			"resolved": False,
			"created_by": "Milly"
		}
	]

	# accounts list
	accounts = [
		{
			"firstname": "Milly",
			"lastname": "Kwamboka",
			"email": "milly@gmail.com",
			"password": 4747,
			"confirm_password": 4747
		}
	]

	# user post request route
	@app.route("/users/api/v1.0/requests/", methods=["POST"])
	def create_request():
		if request.json:
			req = {
				"id": requests[-1]["id"] + 1,
				"title": request.json.get('title', ''),
				"description": request.json.get('description', ''),
				"location": request.json.get('location', ''),
				"approved": False,
				"rejected": False,
				"resolved": False,
				"created_by": request.json.get('created_by', '')
			}
			requests.append(req)
			return jsonify({
				"id": req["id"],
				"description": req["description"],
				"location": req["location"],
				"approved": req["approved"],
				"rejected": req["rejected"],
				"resolved": req["resolved"],
				"created_by": req["created_by"]
			}), 201

	# user account registration view
	@app.route("/users/api/v1.0/account/register/", methods=["POST"])
	def create_account():
		if request.json:
			user = {
				"firstname": request.json.get('firstname', ''),
				"lastname": request.json.get('lastname', ''),
				"email": request.json.get('email', ''),
				"password": request.json.get('password', ''),
				"confirm_password": request.json.get('confirm_password', '')
			}
			accounts.append(user)
			return jsonify({
				"message": "Your account was created successfully."
			}), 201

	# user login view
	@app.route("/users/api/v1.0/authenticate/", methods=["POST"])
	def login_user():
		if request.json:
			user = {
				"email": request.json.get('email', ''),
				"password": request.json.get('password', '')
			}
			for account in accounts:
				if account["email"] == user["email"]:
					if account["password"] == user["password"]:
						return jsonify({
							"status": "Success",
							"message": "Login was successfull",
							"email": account["email"]
						}), 200
					return jsonify({
						"message": "Invalid password"
					}), 401
			return jsonify({
				"message": "Invalid credentials"
			}), 401

	# get requests view for a user
	@app.route("/users/api/v1.0/requests/", methods=["GET"])
	def get_requests():
		name = request.headers["name"]
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

	# get request view for user
	@app.route("/users/api/v1.0/requests/<int:id>/", methods=["GET"])
	def get_request(id):
		name = request.headers["name"]
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

	return app
