"""
Minimal URL configuration for basic Django deployment
Only includes Django built-in URLs - no custom apps
"""

from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.shortcuts import render

def home_view(request):
    """Simple home page view"""
    return HttpResponse("""
    <html>
    <head><title>Kenyan Payroll Management System</title></head>
    <body>
        <h1>🎉 Deployment Successful!</h1>
        <p>Your Django application is running on Render.</p>
        <p><a href="/admin/">Go to Admin Panel</a></p>
        <hr>
        <p><em>Basic deployment - custom features will be added incrementally.</em></p>
    </body>
    </html>
    """)

urlpatterns = [
    # Home page
    path('', home_view, name='home'),
    
    # Django admin
    path('admin/', admin.site.urls),
]
