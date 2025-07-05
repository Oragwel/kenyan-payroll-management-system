"""
Security middleware for the payroll system
"""
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.template.response import TemplateResponse


class PayrollSecurityMiddleware:
    """
    Middleware to enforce authentication and authorization for payroll routes
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Define public URLs that don't require authentication
        self.public_urls = [
            '/',
            '/login/',
            '/logout/',
            '/admin/login/',
            '/admin/logout/',
            '/admin/password_change/',
            '/admin/password_change/done/',
            '/admin/jsi18n/',
        ]
        
        # Define admin-only URL patterns
        self.admin_only_patterns = [
            '/admin/',
            '/payroll/generate/',
            '/payroll/periods/',
            '/payroll/payslip/generate/',
            '/employees/create/',
            '/employees/',  # Employee list requires login
            '/admin/payroll/',
        ]
        
        # Define staff-only URL patterns
        self.staff_only_patterns = [
            '/payroll/generation/',
            '/payroll/periods/',
            '/admin/dashboard/',
            '/admin/reports/',
            '/admin/settings/',
        ]

    def __call__(self, request):
        # Check if the URL requires authentication
        if self.requires_authentication(request.path):
            if not request.user.is_authenticated:
                # Store the attempted URL for redirect after login
                request.session['next'] = request.get_full_path()
                messages.warning(request, 'Please log in to access this page.')
                return redirect('login')
            
            # Check if the URL requires staff privileges
            if self.requires_staff_access(request.path):
                if not request.user.is_staff:
                    return self.render_403(request, 'Staff access required for this page.')
            
            # Check if the URL requires admin privileges
            if self.requires_admin_access(request.path):
                if not (request.user.is_staff or request.user.is_superuser):
                    return self.render_403(request, 'Administrator access required for this page.')

        response = self.get_response(request)
        return response

    def requires_authentication(self, path):
        """Check if a path requires authentication"""
        # Allow public URLs
        if path in self.public_urls:
            return False
            
        # Allow static files and media
        if path.startswith('/static/') or path.startswith('/media/'):
            return False
            
        # Allow Django admin static files
        if path.startswith('/admin/jsi18n/') or path.startswith('/admin/r/'):
            return False
            
        # All other paths require authentication
        return True

    def requires_staff_access(self, path):
        """Check if a path requires staff access"""
        for pattern in self.staff_only_patterns:
            if path.startswith(pattern):
                return True
        return False

    def requires_admin_access(self, path):
        """Check if a path requires admin access"""
        # Payroll generation and sensitive operations
        sensitive_patterns = [
            '/payroll/payslip/generate/',
            '/payroll/generate/',
            '/employees/create/',
            '/employees/',
            '/admin/payroll/users/',
            '/admin/payroll/organizations/',
        ]
        
        for pattern in sensitive_patterns:
            if path.startswith(pattern):
                return True
        return False

    def render_403(self, request, message):
        """Render a 403 Forbidden page with custom message"""
        context = {
            'error_message': message,
            'user': request.user,
        }
        return TemplateResponse(request, '403.html', context, status=403)


class PayrollPermissionMiddleware:
    """
    Additional middleware for role-based permissions
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Add user role information to request
        if request.user.is_authenticated:
            # Import here to avoid circular imports
            from employees.user_management import PayrollRoleManager
            request.user.payroll_role = PayrollRoleManager.get_user_role(request.user)
        
        response = self.get_response(request)
        return response


class SecureHeadersMiddleware:
    """
    Add security headers to all responses
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Add CSP header for additional security
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "font-src 'self' https://cdn.jsdelivr.net; "
            "img-src 'self' data:; "
            "connect-src 'self';"
        )
        
        return response
