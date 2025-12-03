# utils.py
import logging
from functools import wraps
from flask import jsonify, request

# Logging setup
logger = logging.getLogger("mini_ecom")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
ch.setFormatter(fmt)
logger.addHandler(ch)

# Custom Exceptions
class APIError(Exception):
    status_code = 400
    def __init__(self, message, status_code=None):
        super().__init__(message)
        if status_code:
            self.status_code = status_code
        self.message = message

class NotFoundError(APIError):
    def __init__(self, message="Resource not found"):
        super().__init__(message, status_code=404)

class ConflictError(APIError):
    def __init__(self, message="Conflict"):
        super().__init__(message, status_code=409)

# Decorator for routes to catch exceptions and log
def api_handler(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except APIError as e:
            logger.error(f"APIError: {e.message}")
            return jsonify({"error": e.message}), e.status_code
        except Exception as e:
            logger.exception("Unhandled exception")
            return jsonify({"error": "Internal Server Error"}), 500
    return wrapper
