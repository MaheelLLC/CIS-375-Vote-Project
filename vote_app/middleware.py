# vote_app/middleware.py

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    """
    Middleware that requires a user to be authenticated to access any view
    except for the specified exempt views.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [reverse('login'), reverse('register')]  # Removed reverse('signup')
        # Add other URLs that should be exempt from login requirement here
        if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
            self.exempt_urls += [url for url in settings.LOGIN_EXEMPT_URLS]

    def __call__(self, request):
        if not request.user.is_authenticated:
            path = request.path_info
            if not any(path.startswith(url) for url in self.exempt_urls):
                return redirect('login')
        response = self.get_response(request)
        return response
