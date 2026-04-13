import logging
from rest_framework.views import exception_handler
from .exceptions import AppError
from rest_framework.response import Response
from rest_framework import status


logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    if isinstance(exc, AppError):
        logger.error(exc.message)
        return Response(status=status.HTTP_409_CONFLICT)

    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data["status_code"] = response.status_code

    return response
