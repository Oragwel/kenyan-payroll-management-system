from django.urls import path
from . import admin_views
from core import admin_views as core_admin_views

app_name = 'admin'

urlpatterns = [
    # Main Admin Dashboard
    path('', core_admin_views.admin_dashboard, name='dashboard'),

    # Organization Management - Obfuscated URLs
    path('entity-management/', admin_views.organization_dashboard, name='organization_dashboard'),
    path('entity-management/new/', admin_views.organization_create, name='organization_create'),
    path('entity-management/<int:org_id>/details/', admin_views.organization_detail, name='organization_detail'),
    path('entity-management/<int:org_id>/modify/', admin_views.organization_edit, name='organization_edit'),
    path('entity-management/<int:org_id>/remove/', admin_views.organization_delete, name='organization_delete'),
    path('entity-management/<int:org_id>/activate/', admin_views.set_default_organization, name='set_default_organization'),

    # User Management - Obfuscated URLs
    path('access-control/', admin_views.user_management_dashboard, name='user_management'),
    path('access-control/new/', admin_views.create_user, name='create_user'),
    path('access-control/<int:user_id>/permissions/', admin_views.edit_user_role, name='edit_user_role'),
    path('access-control/<int:user_id>/status/', admin_views.toggle_user_status, name='toggle_user_status'),
    path('access-control/<int:user_id>/remove/', admin_views.delete_user, name='delete_user'),
    path('access-control/initialize/', admin_views.initialize_roles, name='initialize_roles'),

    # System Management - Obfuscated URLs
    path('system-config/', admin_views.system_settings, name='system_settings'),
    path('initial-setup/', admin_views.quick_setup_wizard, name='quick_setup_wizard'),
    path('analytics/', core_admin_views.admin_reports, name='reports'),
]
