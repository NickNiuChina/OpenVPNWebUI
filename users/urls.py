from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    # path("", include("django.contrib.auth.urls")),
    path("", views.users, name='users'),
    # path("logout/", views.logout, name='logout'),
]