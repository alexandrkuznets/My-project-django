import datetime

from django.http import HttpRequest
from django.core.exceptions import PermissionDenied


def set_useragent_on_request_middleware(get_response):

    print("initial call")

    def middleware(request: HttpRequest):
        print("before get response")
        request.user_agent =request.META.get("HTTP_USER_AGENT", "unknown")
        response = get_response(request)
        print("after get response")
        return response

    return middleware


class CountRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        self.requests_count += 1
        print("request count", self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        print("response count", self.responses_count)

        return response

    def process_exception(self, requset: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print("got", self.exceptions_count, "exception so far")





class ThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.users = {}

    def __call__(self, request: HttpRequest):
        if request.META['REMOTE_ADDR'] in self.users:
            if self.users[f"{request.META['REMOTE_ADDR']}"]["count"] > 5:
                self.users[f"{request.META['REMOTE_ADDR']}"]["count"] = 0
                raise PermissionDenied("The site visit limit has been exceeded")

            self.users[f"{request.META['REMOTE_ADDR']}"]["count"] += 1
        else:
            self.users[f"{request.META['REMOTE_ADDR']}"] = {"count": 0}

        response = self.get_response(request)
        return response


