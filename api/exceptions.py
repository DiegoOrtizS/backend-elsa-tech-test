from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc: Exception, context: dict | None) -> Response:
    response = exception_handler(exc, context)
    if isinstance(exc, ObjectDoesNotExist):
        return Response(
            {"statusCode": 404, "message": f"{str(exc).split(' ')[0]} not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    return response
