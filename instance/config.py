"""
Configurations variable
"""
class Config(object):
    """
    Parent configurations class
    """
    DEBUG = False

class Development(Config):
    """
    Development configurations class
    """
    DEBUG = True

class Testing(Config):
    """
    Testing configurations class
    """
    DEBUG = True
    TESTING = True

class Production(Config):
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
