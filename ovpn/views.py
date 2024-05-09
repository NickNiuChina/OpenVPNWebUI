from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages


def index(request):
    # messages.success(request, 'The flash messages show successfully.')
    return render(request, 'ovpn/main.html', {'session_data': request.session})
