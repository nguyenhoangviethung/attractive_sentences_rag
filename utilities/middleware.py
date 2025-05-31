import os
from functools import wraps
from flask import request


class MiddleWare:
    
    @staticmethod
    def check_permission(f):
        SECRET_ADMIN_TOKEN = os.getenv('SECRET_ADMIN')
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth = request.headers.get("Authorization")
            if auth == f"Bearer {SECRET_ADMIN_TOKEN}":
                return f(*args, is_authorized=True, **kwargs)
            return f(*args, is_authorized=False, **kwargs)
        return wrapper
