from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 排除不需要登录就能访问的页面
        if request.path_info in ["/auth/login/", "/image/code"]: # 获取当前用户请求的 url
            return None
        # 读取当前访问用户的 session 信息
        info_dict = request.session.get("authenticated")
        if info_dict:
            return None
        # Redirect to login page
        return redirect('authentication:login')

    def process_response(self, request, response):
        return response
