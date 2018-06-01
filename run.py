"""
Run application from here
"""
import os

from app import create_app

CONFIG_NAME = os.getenv("FLASK_ENV")

APP = create_app(CONFIG_NAME)

if __name__ == '__main__':
    APP.run()
