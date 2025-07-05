from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib import messages


def public_landing(request):
    """Public landing page for unauthorized users"""
    # If user is already authenticated, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    return render(request, 'public/landing.html')


@login_required
def dashboard(request):
    """Protected dashboard for authenticated users"""
    # Import here to avoid circular imports
    from employees.models import Employee, Department, JobTitle
    from payroll_processing.models import PayrollPeriod, Payslip
    
    # Get dashboard statistics
    context = {
        'total_employees': Employee.objects.filter(is_active=True).count(),
        'total_departments': Department.objects.count(),
        'total_job_titles': JobTitle.objects.count(),
        'recent_payroll_periods': PayrollPeriod.objects.order_by('-created_at')[:3],
        'user': request.user,
    }
    
    # Add admin-specific stats
    if request.user.is_staff:
        context.update({
            'total_payroll_periods': PayrollPeriod.objects.count(),
            'total_payslips': Payslip.objects.count(),
            'pending_salary_structures': Employee.objects.filter(
                is_active=True, 
                salary_structure__isnull=True
            ).count(),
        })
    
    return render(request, 'dashboard.html', context)


class CustomLoginView(auth_views.LoginView):
    """Custom login view with redirect logic and enhanced security"""
    template_name = 'registration/login.html'

    def dispatch(self, request, *args, **kwargs):
        """Add security headers to prevent password saving"""
        response = super().dispatch(request, *args, **kwargs)

        # Add security headers to prevent caching and password saving
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        response['X-Frame-Options'] = 'DENY'
        response['X-Content-Type-Options'] = 'nosniff'
        response['Referrer-Policy'] = 'no-referrer'
        response['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=(), payment=()'

        # Content Security Policy to prevent password manager injection
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "font-src 'self' https://cdn.jsdelivr.net; "
            "img-src 'self' data:; "
            "connect-src 'self'; "
            "form-action 'self'; "
            "frame-ancestors 'none';"
        )

        return response

    def get_success_url(self):
        # Always redirect to dashboard after successful login, regardless of user type
        return '/dashboard/'

    def form_valid(self, form):
        # Add success message
        messages.success(self.request, f'Welcome back, {form.get_user().username}!')
        response = super().form_valid(form)

        # Clear any potential cached credentials
        response['Clear-Site-Data'] = '"cache", "storage"'

        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)


class CustomLogoutView(auth_views.LogoutView):
    """Custom logout view"""
    
    def get_next_page(self):
        # Redirect to public landing page after logout
        messages.success(self.request, 'You have been successfully logged out.')
        return '/'
