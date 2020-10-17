from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler


def drf_exception_handler(exc, context):
    if not isinstance(exc, ValidationError):
        exc_detail = {'error': exc}
        exc = ValidationError(detail=exc_detail)

    response = exception_handler(exc, context)
    return response
