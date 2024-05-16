from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages


def index(request):
    # messages.success(request, 'The flash messages show successfully.')
    return render(request, 'ovpn/main.html')


def users(request):
    return render(request, 'ovpn/users.html')


def show_settings(request):
    res = ''
    from django.conf import settings
    for name in dir(settings):
        if not name.startswith("_"):
            res += '</br>'
            res += str(name)
            res += ':'
            res += str(getattr(settings, name))
    return HttpResponse(res)


def show_sessions(request):
    res = ''
    for key, value in request.session.items():
        res += '</br>'
        res += str(key)
        res += ':'
        res += str(value)
    return HttpResponse(res)