from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    # path("", include("django.contrib.auth.urls")),
    path("", views.users, name='users'),
    path('delete', views.user_delete, name='user_delete'),
    path('update/<uuid:sid>/', views.user_update, name='user_update'),
    # path("logout/", views.logout, name='logout'),
]