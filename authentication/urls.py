"""
URL configuration for OpenVPNWebUI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from . import views

""" django.contrib.auth.urls -
    auth/ login/ [name='login']
    auth/ logout/ [name='logout']
    auth/ password_change/ [name='password_change']
    auth/ password_change/done/ [name='password_change_done']
    auth/ password_reset/ [name='password_reset']
    auth/ password_reset/done/ [name='password_reset_done']
    auth/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
    auth/ reset/done/ [name='password_reset_complete']
"""

urlpatterns = [
    # path("", include("django.contrib.auth.urls")),
    path("login/", views.login, name='login'),
]

