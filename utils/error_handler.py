from flask import make_response, request


def error_handler(func):
    def wrapper(*args, **kwargs):

        try:
            return func(*args, **kwargs)
        except Exception as e:
            return make_response({"status": False, "detail": str(e)}, 400)

    return wrapper