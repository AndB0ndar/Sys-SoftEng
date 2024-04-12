from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:
    """
    Middleware for enforcing login requirements on specific URLs.

    This middleware redirects unauthenticated users to the login page when they attempt to access
    URLs other than those explicitly allowed (e.g., login and registration pages).

    Attributes:
    - get_response: Callable representing the next middleware or view in the request-response cycle.
    """
    def __init__(self, get_response):
        """
        Initializes the LoginRequiredMiddleware instance.

        Parameters:
        - get_response: Callable representing the next middleware or view in the request-response cycle.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Process the incoming request.

        If the user is not authenticated and the requested URL is not in the allowed URLs list,
        redirects the user to the login page.

        Parameters:
        - request: HttpRequest object representing the incoming request.

        Returns:
        - HttpResponse object representing the response to the request.
        """
        allowed_urls = [reverse('login'), reverse('register')]
        response = self.get_response(request)
        if not request.user.is_authenticated and request.path not in allowed_urls:
            return redirect(reverse('login'))
        return response

