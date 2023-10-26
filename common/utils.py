from django.utils import timezone
from rest_framework.request import Request

from common.exceptions import MissingMandatoryParameterException


####################
# Request Decorator
####################
def mandatory_key(request: Request, name: str) -> any:
    try:
        if request.method == "GET":
            data = request.GET[name]
        else:
            data = request.POST[name]
        if data in ["", None]:
            raise MissingMandatoryParameterException()
    except Exception:
        try:
            json_body = request.data
            data = json_body[name]
            if data in ["", None]:
                raise MissingMandatoryParameterException()
        except Exception:
            raise MissingMandatoryParameterException()

    return data


def optional_key(request: Request, name: str, default_value="") -> any:
    try:
        if request.method == "GET":
            data = request.GET[name]
        else:
            data = request.POST[name]
        if data in ["", None]:
            data = default_value
    except Exception:
        try:
            json_body = request.data
            data = json_body[name]
            if data in ["", None]:
                data = default_value
        except Exception:
            data = default_value
    return data


####################
# Date
####################
def get_now() -> timezone:
    return timezone.now().strftime("%Y-%m-%d")


def get_before_week() -> timezone:
    return (timezone.now() - timezone.timedelta(days=7)).strftime("%Y-%m-%d")
