from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django import forms
from users.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.utils.encoding import force_bytes, force_str
from django.core.signing import Signer, SignatureExpired


class LoginForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return make_password(pwd)


def login(request, next=None):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'auth/login.html', {"form": form})
    # form = LoginForm(data=request.POST)
    data = request.POST
    # print(data)
    # if form.is_valid():

    # Cookie
    signed_cookie = Signer()
    try:
        user_id = force_str(signed_cookie.unsign(request.COOKIES["auth_cookie"]))
        print("user_id: " + user_id)
    except (KeyError, SignatureExpired):
        # Cookie invalid
        pass
    else:
        # Make sure the new is still in db
        user = User.objects.filter(id=user_id).first()
        if user:
            request.session["authenticated"] = {"id": str(user.id), "username": user.username, "group": str(user.group)}
            return redirect('ovpn:index')
        else:
            # User does not exist
            pass

    username = request.POST.get('username')
    password = request.POST.get('password')
    user = User.objects.filter(username=username).first()
    redirect_url = request.POST.get("next")

    if username and password and user:
        if check_password(password, user.password):
            # create session
            request.session["authenticated"] = {"id": str(user.id), "username": username, "group": str(user.group)}
            if request.POST.get('remember') == 'on':
                # for seven days
                request.session["authenticated"].update({'remember': 'on'})
                request.session.set_expiry(60 * 60 * 24 * 7)
            if redirect_url in ["/", reverse('authentication:login')]:
                return redirect('ovpn:index')
            else:
                # Create cookie
                signed_cookie = Signer()
                # cookie_key = 'auth_cookie_%s' % user.id
                cookie_value = signed_cookie.sign(force_str(user.id))
                response = redirect(redirect_url)
                response.set_cookie("auth_cookie", cookie_value, max_age=60*60*24*7)

                return response

        else:
            messages.error(request, "Username or password is not correct!")
            return render(request, 'auth/login.html')
    else:
        pass
    # return render(request, 'auth/login.html', {"form": form})
    messages.error(request, "Username or password is not correct!!")
    return render(request, 'auth/login.html')


def logout(request):
    del request.session['authenticated']
    return redirect("authentication:login")

# 图片验证码
# from appback.util.Verification_Code import Verification_Code
# from io import BytesIO
#
#
# def image_code(request):
#     img, code_str = Verification_Code()
#     print(code_str)
#     request.session["image_code"] = code_str  # 讲图片验证码写入到 session 中
#     request.session.set_expiry(60)  # 设置 60s 超时
#     stream = BytesIO()
#     img.save(stream, 'png')  # 把图片内容写入到内存中
#     return HttpResponse(stream.getvalue())
