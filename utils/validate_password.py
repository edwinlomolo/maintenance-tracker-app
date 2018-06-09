"""
Validate password
"""
import re

def validate_password(password):
    """
    Check if password length is atleast 8 ,contains uppercase
    and lowercase letter, and contains atleast a number
    """
    if len(password) < 8:
        return False
    elif re.search('[0-9]', password) is None:
        return False
    elif re.search('[A-Z]', password) is None:
        return False
    elif re.search('[a-z]', password) is None:
        return False
    else:
        return True
