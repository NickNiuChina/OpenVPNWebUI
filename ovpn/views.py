from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from .models import Servers
import platform
import datetime


def index(request):
    system_info = {
        'system_type': platform.system(),
        'system_version': platform.version(),
        'system_time': datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"),
        }
    return render(request, 'ovpn/main.html')


def servers(request):
    servers = Servers.objects.all()
    return render(request, 'ovpn/servers.html', {"servers": servers})


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