from django.http import HttpRequest

from shareapp.users.models import UserAgent


class UserAgentLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request: HttpRequest):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user.is_authenticated:
            user_agent = request.headers.get("User-Agent")
            user = request.user
            UserAgent.objects.update_or_create(
                user=user,
                defaults={"user_agent": user_agent or "Empty User-Agent value!"},
            )

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
