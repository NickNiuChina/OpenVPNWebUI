from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages


def index(request):
    request.session['username'] = 'super'
    request.session['user_type'] = 1

    # messages.success(request, 'The flash messages show successfully.')
    return render(request, 'ovpn/main.html', {'session_data': request.session})
