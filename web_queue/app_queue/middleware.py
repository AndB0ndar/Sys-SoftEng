from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:
    """
    Middleware for enforcing login requirements on specific URLs.

    This middleware redirects unauthenticated users to the login page when they attempt to access
    URLs other than those explicitly allowed (e.g., login and registration pages).
    """
    def __init__(self, get_response):
        """
        Initialize the middleware.

        :param get_response: A callable that takes a request and returns a response.
        :type get_response: callable
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Process incoming requests.

        :param request: The incoming request.
        :type request: django.http.HttpRequest
        :return: A response.
        :rtype: django.http.HttpResponse
        """
        allowed_urls = [reverse('login'), reverse('register')]
        response = self.get_response(request)
        if not request.user.is_authenticated and request.path not in allowed_urls:
            return redirect(reverse('login'))
        return response
