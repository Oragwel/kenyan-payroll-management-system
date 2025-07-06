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

# Configure admin site to use our custom login and logout
admin.site.login_url = '/admin/login/'
admin.site.logout_url = '/admin/logout/'
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
from core.views import public_landing, dashboard
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse, HttpResponseRedirect

@csrf_exempt
def simple_login(request):
    """Simple CSRF-exempt login for frontend"""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # Debug logging
        print(f"🔍 Frontend login attempt - Username: '{username}', Password length: {len(password) if password else 0}")

        # Validate input
        if not username:
            print("❌ No username provided")
            return HttpResponse('Username is required', status=400)

        if not password:
            print("❌ No password provided")
            return HttpResponse('Password is required', status=400)

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

            # Always redirect to dashboard for frontend login
            print(f"🔄 Frontend login - Redirecting to dashboard")
            return HttpResponseRedirect('/dashboard/')
        else:
            print(f"❌ Authentication failed for {username}")
            return HttpResponse(f'Invalid credentials for user "{username}". Check password.', status=401)
    else:
        # GET request - show the login form
        context = {
            'title': 'System Login',
            'site_header': 'Payroll System Login',
        }
        return render(request, 'registration/login.html', context)

@csrf_exempt
def admin_login(request):
    """CSRF-exempt login specifically for Django admin"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Debug logging
        print(f"🔍 Admin login attempt - Username: '{username}', Password length: {len(password) if password else 0}")

        # Check if user exists
        from django.contrib.auth.models import User
        try:
            db_user = User.objects.get(username=username)
            print(f"✅ User found in database: {db_user.username}, Active: {db_user.is_active}, Staff: {db_user.is_staff}")

            # Check if user has admin access
            if not db_user.is_staff:
                print(f"❌ User '{username}' is not staff - cannot access admin")
                return HttpResponse(f'User "{username}" does not have admin access', status=403)

        except User.DoesNotExist:
            print(f"❌ User '{username}' not found in database")
            return HttpResponse(f'User "{username}" not found in database', status=401)

        # Try authentication
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(f"✅ Admin authentication successful for {username}")
            auth_login(request, user)

            # Get next URL or default to Django admin home
            next_url = request.POST.get('next') or request.GET.get('next')

            # Ensure we redirect to a valid admin URL
            if next_url:
                # If next_url is just '/admin/', it's valid
                if next_url == '/admin/' or next_url.startswith('/admin/') and not next_url.startswith('/admin/dashboard'):
                    redirect_url = next_url
                else:
                    redirect_url = '/admin/'
            else:
                redirect_url = '/admin/'

            print(f"🔄 Admin login - Redirecting to: {redirect_url}")
            return HttpResponseRedirect(redirect_url)
        else:
            print(f"❌ Admin authentication failed for {username}")
            return HttpResponse(f'Invalid admin credentials for user "{username}". Check password.', status=401)
    else:
        # Show admin login template
        next_url = request.GET.get('next', '/admin/')
        context = {
            'next': next_url,
            'site_header': 'Payroll System Administration',
            'site_title': 'Admin Login',
            'title': 'Log in to Admin Panel'
        }
        return render(request, 'admin/login.html', context)

@csrf_exempt
def smart_logout(request):
    """Smart logout that redirects based on context (admin vs frontend)"""
    from django.contrib.auth import logout
    from django.contrib import messages

    print(f"🔍 Logout request from user: {request.user.username if request.user.is_authenticated else 'Anonymous'}")

    # Determine where the logout request came from
    referer = request.META.get('HTTP_REFERER', '')
    next_url = request.GET.get('next', '')

    # Check if logout came from Django admin
    is_admin_logout = (
        '/admin/' in referer or
        '/admin/' in next_url or
        request.path.startswith('/admin/') or
        'admin' in request.GET.get('from', '') or
        request.path == '/admin/logout/'
    )

    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        print(f"✅ User '{username}' logged out successfully")

        if is_admin_logout:
            print(f"🔄 Admin logout detected - redirecting to Django admin login")
            # Don't add messages for admin logout (admin handles its own messages)
            return HttpResponseRedirect('/admin/login/')
        else:
            print(f"🔄 Frontend logout detected - redirecting to public landing page")
            messages.success(request, f'You have been successfully logged out.')
            return HttpResponseRedirect('/')
    else:
        # User not authenticated
        if is_admin_logout:
            print(f"🔄 Unauthenticated admin access - redirecting to Django admin login")
            return HttpResponseRedirect('/admin/login/')
        else:
            print(f"🔄 Unauthenticated frontend access - redirecting to public landing page")
            return HttpResponseRedirect('/')

urlpatterns = [
    # Public landing page (no authentication required)
    path('', public_landing, name='public_landing'),

    # Authentication URLs - CSRF exempt for debugging
    path('login/', simple_login, name='login'),  # Frontend login
    path('logout/', smart_logout, name='logout'),  # Smart logout (admin vs frontend)
    path('clear-passwords/', lambda request: render(request, 'registration/clear_saved_passwords.html'), name='clear_passwords'),

    # Protected dashboard (authentication required)
    path('dashboard/', dashboard, name='dashboard'),
    path('home/', dashboard, name='home'),  # Alias for backward compatibility

    # Admin interface - with custom login and logout
    path('admin/login/', admin_login, name='admin_login'),  # CSRF-exempt login for admin
    path('admin/logout/', lambda request: smart_logout(request), name='admin_logout'),  # Admin logout
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
