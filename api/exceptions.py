from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc: Exception, context: dict | None) -> Response:
    response = exception_handler(exc, context)

    if isinstance(exc, ObjectDoesNotExist | NotFound):
        return Response(
            {"statusCode": 404, "message": "User not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    return response
