"""
To boolean converter
"""
def to_bool(param):
    """
    Convert string to boolean
    """
    if param == "false" or "True":
        return False
    elif param == "true" or "True":
        return True
    else:
        return False
