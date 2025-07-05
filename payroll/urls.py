"""payroll URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.shortcuts import redirect, render
from django.conf import settings
from django.conf.urls.static import static
from core.views import public_landing, dashboard, CustomLoginView, CustomLogoutView

urlpatterns = [
    # Public landing page (no authentication required)
    path('', public_landing, name='public_landing'),

    # Authentication URLs
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('clear-passwords/', lambda request: render(request, 'registration/clear_saved_passwords.html'), name='clear_passwords'),

    # Protected dashboard (authentication required)
    path('dashboard/', dashboard, name='dashboard'),
    path('home/', dashboard, name='home'),  # Alias for backward compatibility

    # Admin interface
    path('admin/', admin.site.urls),  # Django admin (will be customized with templates)
    path('admin/payroll/', include('employees.admin_urls', namespace='payroll_admin')),

    # Secure access URLs (token-based authentication) - Temporarily disabled
    # path('secure/', include('core.secure_urls', namespace='secure')),

    # Protected application URLs (authentication required)
    path('', include('core.urls', namespace='core')),
    path('employees/', include('employees.urls', namespace='employees')),
    path('payroll/', include('payroll_processing.urls', namespace='payroll_processing')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
