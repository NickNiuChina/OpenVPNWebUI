from django.shortcuts import redirect, reverse
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):

        # pages does not need login
        if request.path_info in [reverse('authentication:login'), "/image/code"]:
            return None

        if str(request.path_info).startswith(reverse('authentication:login').rstrip('/')):
            return redirect(reverse('authentication:login'))

        # 读取当前访问用户的 session 信息
        info_dict = request.session.get("authenticated")
        if info_dict:
            return None

        # Redirect to login page
        redirect_url = reverse('authentication:login')
        # return redirect('authentication:login')
        return redirect(f'{redirect_url}?next={request.path}')

    def process_response(self, request, response):
        return response
