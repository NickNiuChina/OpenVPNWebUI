from django.shortcuts import redirect, reverse
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware1(MiddlewareMixin):
    """ Django 1.10-style middleware

    Args:
        MiddlewareMixin (MiddlewareMixin): Deprecated class to implement compatibility.
    """
    def process_request(self, request):

        # pages does not need login
        if request.path_info in [reverse('authentication:login'), "/image/code"]:
            return None

        if str(request.path_info).startswith(reverse('authentication:login').rstrip('/')):
            return redirect(reverse('authentication:login'))

        # Read session
        info_dict = request.session.get("authenticated")
        if info_dict:
            return None

        # Redirect to login page
        redirect_url = reverse('authentication:login')
        # return redirect('authentication:login')
        return redirect(f'{redirect_url}?next={request.path}')

    def process_response(self, request, response):
        return response
    
class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before the view (and later middleware) are called.
        #print('--process_request--')

        response = self.get_response(request)

        # Code to be executed for each request/response after the view is called.
        #print('--process_response')

        return response

    def process_view(cls, request, view_func, *view_args, **view_kwargs):
        # pages does not need login
        if request.path_info in [reverse('authentication:login'), "/image/code"]:
            return None

        if str(request.path_info).startswith(reverse('authentication:login').rstrip('/')):
            return redirect(reverse('authentication:login'))

        # Read session
        info_dict = request.session.get("authenticated")
        if info_dict:
            return None

        # Redirect to login page
        redirect_url = reverse('authentication:login')
        # return redirect('authentication:login')
        return redirect(f'{redirect_url}?next={request.path}')
