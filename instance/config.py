"""
Configurations variable
"""
import os

class Config(object): # pylint: disable=too-few-public-methods
    """
    Parent configurations class
    """
    DEBUG = False
    TESTING = False
    HOST = os.getenv("HOST")
    DATABASE = os.getenv("DATABASE")
    USER = os.getenv("USER")
    PASS = os.getenv("PASS")

class Development(Config): # pylint: disable=too-few-public-methods
    """
    Development configurations class
    """
    DEBUG = True

class Testing(Config): # pylint: disable=too-few-public-methods
    """
    Testing configurations class
    """
    DEBUG = False
    TESTING = True
    HOST = os.getenv("HOST")
    DATABASE = os.getenv("TEST_DATABASE")
    USER = os.getenv("USER")
    PASS = os.getenv("PASS")

class Production(Config): # pylint: disable=too-few-public-methods
    """
    Production configurations class
    """
    TESTING = True
    DEBUG = False

APP_CONFIG = {
    "development": Development,
    "testing": Testing,
    "production": Production
}
