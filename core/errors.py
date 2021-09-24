from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler
from rest_framework_simplejwt.exceptions import InvalidToken


def drf_exception_handler(exc, context):
    if not isinstance(exc, ValidationError):
        if isinstance(exc, InvalidToken):
            exc_detail = {"token": [exc.args[0]["detail"]]}
        else:
            exc_detail = {"error": [exc]}
        exc = ValidationError(detail=exc_detail)

    response = exception_handler(exc, context)
    return response
