from rest_framework import status
from rest_framework.exceptions import APIException


class MissingMandatoryParameterException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Missing mandatory parameter"
    default_code = "missing_mandatory_parameter"


class InvalidParameterException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid parameter"
    default_code = "invalid_parameter"


class UnknownServerErrorException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Unknown server error"
    default_code = "unknown_server_error"


class InvalidPasswordException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid password"
    default_code = "Invalid password"
