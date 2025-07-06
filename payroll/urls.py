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

# Configure admin site to use our custom login
admin.site.login_url = '/admin/login/'
from django.shortcuts import redirect, render
from django.conf import settings
from django.conf.urls.static import static
from core.views import public_landing, dashboard, CustomLoginView, CustomLogoutView
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse, HttpResponseRedirect

@csrf_exempt
def simple_login(request):
    """Simple CSRF-exempt login for debugging"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Debug logging
        print(f"🔍 Login attempt - Username: '{username}', Password length: {len(password) if password else 0}")

        # Check if user exists
        from django.contrib.auth.models import User
        try:
            db_user = User.objects.get(username=username)
            print(f"✅ User found in database: {db_user.username}, Active: {db_user.is_active}")
        except User.DoesNotExist:
            print(f"❌ User '{username}' not found in database")
            return HttpResponse(f'User "{username}" not found in database', status=401)

        # Try authentication
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(f"✅ Authentication successful for {username}")
            auth_login(request, user)

            # Check if this is an admin login (from admin interface)
            next_url = request.POST.get('next') or request.GET.get('next')
            referer = request.META.get('HTTP_REFERER', '')
            current_path = request.path

            print(f"🔍 Login context - Path: {current_path}, Next: {next_url}, Referer: {referer}")

            # If accessed via /admin/login/ or next URL contains admin, go to admin
            if '/admin/login/' in current_path or (next_url and '/admin/' in next_url) or '/admin/' in referer:
                admin_redirect = next_url if next_url and '/admin/' in next_url else '/admin/'
                print(f"🔄 Admin login detected - Redirecting to: {admin_redirect}")
                return HttpResponseRedirect(admin_redirect)
            elif next_url:
                print(f"🔄 Custom redirect to: {next_url}")
                return HttpResponseRedirect(next_url)
            else:
                print(f"🔄 Frontend login - Redirecting to dashboard")
                return HttpResponseRedirect('/dashboard/')
        else:
            print(f"❌ Authentication failed for {username}")
            return HttpResponse(f'Invalid credentials for user "{username}". Check password.', status=401)
    else:
        return render(request, 'registration/login.html')

urlpatterns = [
    # Public landing page (no authentication required)
    path('', public_landing, name='public_landing'),

    # Authentication URLs - temporarily CSRF exempt for debugging
    path('login/', simple_login, name='login'),
    path('login-django/', csrf_exempt(auth_views.LoginView.as_view(
        template_name='registration/login.html',
        success_url='/dashboard/'
    )), name='login_django'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('clear-passwords/', lambda request: render(request, 'registration/clear_saved_passwords.html'), name='clear_passwords'),

    # Protected dashboard (authentication required)
    path('dashboard/', dashboard, name='dashboard'),
    path('home/', dashboard, name='home'),  # Alias for backward compatibility

    # Admin interface - with custom login
    path('admin/login/', simple_login, name='admin_login'),  # CSRF-exempt login for admin
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
