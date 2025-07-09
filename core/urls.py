from django.urls import path
from django.shortcuts import render
from . import views, admin_views

app_name = 'core'

urlpatterns = [
    # Health check (no authentication required)
    path('health/', views.health_check, name='health_check'),

    # Public views
    path('', views.public_landing, name='public_landing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('mobile-demo/', lambda request: render(request, 'mobile_demo.html'), name='mobile_demo'),

    # Admin views
    path('admin/dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('admin/reports/', admin_views.admin_reports, name='admin_reports'),
    path('admin/settings/', admin_views.admin_settings, name='admin_settings'),
    path('admin/redirect/', admin_views.admin_redirect, name='admin_redirect'),
]
