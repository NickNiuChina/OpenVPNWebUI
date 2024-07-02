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
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    
    path('servers', views.servers, name='servers'),
    path('servers/delete', views.server_delete, name='server_delete'),
    path('servers/update/<uuid:sid>/', views.server_update, name='server_update'),
    path('servers/config/<uuid:sid>/', views.ServerConfigView.as_view(), name='server_config'),
    
    # openvpn client list
    path('<str:ovpn_service>/clients', views.clients, name='clients'),
    path('<str:ovpn_service>/generate_cert', views.GenerateCertView.as_view(), name='generate_cert'),
    path('<str:ovpn_service>/plain_certs', views.PlainCertsView.as_view(), name='plain_certs'),
    path('<str:ovpn_service>/plain_cert/<str:cert_file>', views.PlainCertView.as_view(), name='plain_cert'),
    path('<str:ovpn_service>/encrypt_certs', views.encrypt_certs, name='encrypt_certs'),
    path('<str:ovpn_service>/encrypt_cert/<str:cert_file>', views.encrypt_certs, name='encrypt_cert'),
    
    # openvpn server logs
    path('<str:ovpn_service>/logs', views.server_logs, name='server_logs'),
    path('<str:ovpn_service>/log/<str:log_file>', views.server_log, name='server_log'),

    # System config urls
    path('system/config', views.system_config, name='system_config'),
    path('show/settings', views.ShowSettingsView.as_view(), name='settings'),
    path('show/sessions', views.ShowSessionsView.as_view(), name='sessions'),
]
