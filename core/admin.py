from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from django.http import HttpResponseRedirect


class PayrollAdminSite(admin.AdminSite):
    """Custom admin site for payroll system"""

    site_header = 'Payroll System Administration'
    site_title = 'System Admin'
    index_title = 'System Administration'
    
    def index(self, request, extra_context=None):
        """Redirect to enhanced dashboard"""
        return HttpResponseRedirect('/admin/dashboard/')
    
    def get_urls(self):
        """Add custom URLs to admin"""
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
        ]
        return custom_urls + urls
    
    def dashboard_view(self, request):
        """Redirect to enhanced dashboard"""
        return HttpResponseRedirect('/admin/dashboard/')


# Create custom admin site instance
payroll_admin_site = PayrollAdminSite(name='payroll_admin')

# Register all models with the custom admin site
from django.apps import apps

def register_all_models():
    """Register all models with the custom admin site"""
    for model in apps.get_models():
        try:
            # Skip models that are already registered
            if not payroll_admin_site._registry.get(model):
                # Get the admin class if it exists
                admin_class = admin.site._registry.get(model)
                if admin_class:
                    payroll_admin_site.register(model, admin_class.__class__)
                else:
                    payroll_admin_site.register(model)
        except admin.sites.AlreadyRegistered:
            pass

# Call the registration function
register_all_models()
