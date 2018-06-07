"""
Configurations variable
"""
class Config(object): # pylint: disable=too-few-public-methods
    """
    Parent configurations class
    """
    DEBUG = False

class Development(Config): # pylint: disable=too-few-public-methods
    """
    Development configurations class
    """
    DEBUG = True

class Testing(Config): # pylint: disable=too-few-public-methods
    """
    Testing configurations class
    """
    DEBUG = True
    TESTING = True

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
