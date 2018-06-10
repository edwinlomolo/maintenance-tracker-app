[![Build Status](https://travis-ci.org/3dw1nM0535/maintenance-tracker-app.svg?branch=develop)](https://travis-ci.org/3dw1nM0535/maintenance-tracker-app)
[![codecov](https://codecov.io/gh/3dw1nM0535/maintenance-tracker-app/branch/develop/graph/badge.svg)](https://codecov.io/gh/3dw1nM0535/maintenance-tracker-app)
[![Coverage Status](https://coveralls.io/repos/github/3dw1nM0535/maintenance-tracker-app/badge.svg)](https://coveralls.io/github/3dw1nM0535/maintenance-tracker-app)

# Maintenance Tracker

Maintenance Tracker App is an application that provides users with ability to reach out
to operations and maintenance department regarding their repairs or maintenance requests
and monitor the status of their requests.

![Maintenance Tracker App](https://res.cloudinary.com/dazskjikr/image/upload/v1527438181/Screenshot_from_2018-05-27_19-09-31.png)

This is the User Interface Roadmap for the App. Shows the layouts for various components of Maintenance
Tracker App.

**NB**: This is not the final Maintenance Tracker App layout. New designs will be picked up along during product development.

The App UI elements are being hosted here [Maintenance Tracker](https://3dw1nm0535.github.io/maintenance-tracker-app-ui/)

### Features
 * Users can create an account and login
 * Users should be able to make repairs or maintenance requests
 * Admin should be able to approve/reject repairs or maintenance requests
 * Admin should be able to mark a request as resolved once it is done
 * Admin should be able to view all repairs or maintenance requests made on the application
 * Admin should be able to filter requests
 * User can view his/her requests
 * Users can be able to edit their requests only if the request is not approved

### Extra Features
 * Users can be able to make a request using their location
 * Users can be able to see if their request is resolved
 * Users can be able to see if their request is rejected
 * Users can be able to see if their request is approved
 * Admin can be able to see where the request was made from

### Technology Stack
 * [Flask](http://flask.pocoo.org/)
 * HTML and CSS(Front End Development)
 * [PostgreSQL](https://www.postgresql.org/)

### Tools
 * [Pivotal Tracker](https://www.pivotaltracker.com/n/projects/2174758) - Project Management Tool
 * [Postman](https://www.getpostman.com/) - Postman makes API development Easy
 * [GitHub](https://github.com/3dw1nM0535/maintenance-tracker-app-ui) - Project tracking and collaboration tool
 * [TravisCI](https://travis-ci.org/3dw1nM0535/maintenance-tracker-app-ui) - Distributed Continuous Integration service used
 to build and testing software projects
 * [Coveralls](https://coveralls.io/jobs/37078082) - Web service used to help track your code coverage over time.
 * [Python](https://www.python.org/) - A Programming language that makes you work quickly and integrate systems more effectively

# Getting Started with Maintenance Tracker API

The following guidelines will get you up and running in no time to start interacting and contributing to Maintenance Tracker.

Before your start, you will need Python on your computer, but you may not need to download it.

First of all check that you don't have python installed in your computer by entering `python` in a command line window. If you see
a response from a Python interpreter it will include a version number in its initial display. Generally any recent version can do. Python makes every attempts to maintain backward compatibility

If you need to download Python, you may as well download the latest stable version. Please see the [Python downloads](https://www.python.org/downloads/) page for the most up to date version of Python 2 and Python 3.

## Installation and Setup

While in your terminal,

Install `pip` - Python package manager

```
sudo apt install python-pip
```

Clone this repository

```
git clone https://github.com/3dw1nM0535/maintenance-tracker-app.git
```

Navigate into the directory of your cloned repository

```
cd maintenance-tracker-app
```

Install `virtualenv` - A tool used to create isolated Python environments

```
pip install virtualenv
```

Create a virtual environment in the directory

```
virtualenv venv
```

Activate the virtual environment

```
. venv/bin/activate
```
(Note the space after the full-stop)

Install the requirements or package dependencies for the project

```
pip install -r requirements.txt
```

While still in your terminal, execute the following commands

```
export FLASK_ENV=development
export FLASK_APP=run.py
```

## Start application

Now run the application by executing the following command

```
flask run
```

Done! You are set to interact with the API endpoints.

## API Endpoints

Maintenance Tracker exposes the following API endpoints. You can test this endpoints using [Postman](https://www.getpostman.com/),
your browser or [Curl](https://curl.haxx.se/).

**Endpoint** | **HTTP Method** | **Resource** | **Access Type** 
-------------|-----------------|--------------|----------------
/api/v1/auth/signup/ | POST | Create account | Public
/api/v1/auth/signin/ | POST | Login | Public
/api/v1/users/requests/ | POST | Create request | Private(Authenticated users only)
/api/v1/users/requests/ | GET | Get requests for logged in user | Private(Authenticated users only)
/api/v1/users/requests/id/ | GET | Get a specific request | Private(Authenticated users only)
/api/v1/users/requests/id/ | PUT | Edit a specific request | Private(Authenticated users only)
/api/v1/requests/ | GET | Get all requests | Private(Admin only)
/api/v1/requests/id/approve/ | PUT | Approve a request | Private(Admin only)
/api/v1/requests/id/reject/ | PUT | Reject a request | Private(Admin only)
/api/v1/requests/id/resolve/ | PUT | Resolve a request | Private(Admin only)

## Run tests

To run tests, press `CTRL+C` to stop the server and execute the following command

```
nosetests --rednose --with-coverage --cover-package=app tests/
```

## Contributing
I appreciate your eagerness to contribute. As the project maintainer, i will start accepting contribution as from 12th June 2018.
I will be reinforcing endpoints and make it scaleable on my end before open sourcing.Thank you for your patience.

## Author

[**Edwin Moses**](https://github.com/3dw1nM0535)

## Acknowledgements

[Andela](https://andela.com) - For giving me the resources to learn and the community for helping in developing Maintenance Tracker

