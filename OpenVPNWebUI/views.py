from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
# Base class view
from django.views import View
# from django.views.generic.base import View


def redirect_index(request):
    return redirect('ovpn:index')


def handler404(request, *args, **argv):
    if request.content_type.find('application/json') > -1:
        response = JsonResponse({'error': 'Not found'}, status=404)
    else:
        response = render(request, '404.html', status=404)
    return response


def handler500(request, *args, **argv):
    if request.content_type.find('application/json') > -1:
        response = JsonResponse({'error': 'Server internal error'}, status=500)
    else:
        response = render(request, '500.html', status=500)
    return response
