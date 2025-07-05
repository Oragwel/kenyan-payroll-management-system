from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.db.models import Q
from .models import Organization, Department
from .forms import OrganizationForm, DepartmentForm
from .user_management import PayrollRoleManager
import os


@staff_member_required
def organization_dashboard(request):
    """Main organization management dashboard"""
    organizations = Organization.objects.all().order_by('organization_type', 'name')
    active_org = Organization.objects.filter(is_active=True).first()
    
    # Get organization statistics
    stats = {
        'total_organizations': organizations.count(),
        'active_organizations': organizations.filter(is_active=True).count(),
        'companies': organizations.filter(organization_type='COMPANY').count(),
        'government': organizations.filter(organization_type='GOVERNMENT').count(),
        'parastatals': organizations.filter(organization_type='PARASTATAL').count(),
        'ngos': organizations.filter(organization_type='NGO').count(),
    }
    
    context = {
        'organizations': organizations,
        'active_org': active_org,
        'stats': stats,
        'title': 'Organization Management Dashboard'
    }
    return render(request, 'admin/organization_dashboard.html', context)


@staff_member_required
def set_default_organization(request, org_id):
    """Set an organization as the default/active one"""
    if request.method == 'POST':
        try:
            # Deactivate all organizations
            Organization.objects.all().update(is_active=False)
            
            # Activate the selected organization
            organization = get_object_or_404(Organization, id=org_id)
            organization.is_active = True
            organization.save()
            
            messages.success(request, f'Successfully set "{organization.name}" as the default organization.')
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': f'{organization.name} is now the default organization'})
                
        except Exception as e:
            messages.error(request, f'Error setting default organization: {str(e)}')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': str(e)})
    
    return redirect('payroll_admin:organization_dashboard')


@staff_member_required
def organization_create(request):
    """Create a new organization"""
    if request.method == 'POST':
        form = OrganizationForm(request.POST, request.FILES)
        if form.is_valid():
            organization = form.save()

            # If this is the first organization, make it active
            if Organization.objects.count() == 1:
                organization.is_active = True
                organization.save()

            messages.success(request, f'Organization "{organization.name}" created successfully.')
            return redirect('payroll_admin:organization_dashboard')
    else:
        form = OrganizationForm()
    
    context = {
        'form': form,
        'title': 'Create New Organization',
        'action': 'Create'
    }
    return render(request, 'admin/organization_form.html', context)


@staff_member_required
def organization_edit(request, org_id):
    """Edit an existing organization"""
    organization = get_object_or_404(Organization, id=org_id)
    
    if request.method == 'POST':
        form = OrganizationForm(request.POST, request.FILES, instance=organization)
        if form.is_valid():
            form.save()
            messages.success(request, f'Organization "{organization.name}" updated successfully.')
            return redirect('payroll_admin:organization_dashboard')
    else:
        form = OrganizationForm(instance=organization)
    
    context = {
        'form': form,
        'organization': organization,
        'title': f'Edit {organization.name}',
        'action': 'Update'
    }
    return render(request, 'admin/organization_form.html', context)


@staff_member_required
def organization_detail(request, org_id):
    """View organization details and manage departments"""
    organization = get_object_or_404(Organization, id=org_id)
    departments = organization.departments.all().order_by('name')
    
    context = {
        'organization': organization,
        'departments': departments,
        'title': f'{organization.name} - Details'
    }
    return render(request, 'admin/organization_detail.html', context)


@staff_member_required
def organization_delete(request, org_id):
    """Delete an organization (with confirmation)"""
    organization = get_object_or_404(Organization, id=org_id)
    
    if request.method == 'POST':
        if organization.departments.exists():
            messages.error(request, f'Cannot delete "{organization.name}" because it has departments. Please delete or reassign departments first.')
        else:
            org_name = organization.name
            organization.delete()
            messages.success(request, f'Organization "{org_name}" deleted successfully.')
        return redirect('payroll_admin:organization_dashboard')
    
    context = {
        'organization': organization,
        'title': f'Delete {organization.name}',
        'departments_count': organization.departments.count()
    }
    return render(request, 'admin/organization_confirm_delete.html', context)


@staff_member_required
def system_settings(request):
    """System-wide settings for the payroll system"""
    active_org = Organization.objects.filter(is_active=True).first()
    
    # Get system configuration
    system_config = {
        'default_organization': active_org,
        'total_organizations': Organization.objects.count(),
        'total_departments': Department.objects.count(),
        'database_path': getattr(settings, 'DATABASES', {}).get('default', {}).get('NAME', 'Unknown'),
        'debug_mode': getattr(settings, 'DEBUG', False),
    }
    
    context = {
        'system_config': system_config,
        'title': 'System Settings'
    }
    return render(request, 'admin/system_settings.html', context)


@staff_member_required
def quick_setup_wizard(request):
    """Quick setup wizard for first-time users"""
    if request.method == 'POST':
        # Handle quick setup form
        org_type = request.POST.get('organization_type', 'COMPANY')
        org_name = request.POST.get('organization_name', '')
        
        if org_name:
            # Create organization with minimal required fields
            organization = Organization.objects.create(
                organization_type=org_type,
                name=org_name,
                short_name=request.POST.get('short_name', ''),
                address_line_1=request.POST.get('address', 'Address Line 1'),
                city=request.POST.get('city', 'Nairobi'),
                country='Kenya',
                phone_number=request.POST.get('phone', '+254 XXX XXX XXX'),
                email=request.POST.get('email', 'info@organization.com'),
                kra_pin=request.POST.get('kra_pin', 'P000000000A'),
                is_active=True
            )
            
            # Create basic departments
            basic_departments = [
                {'name': 'Administration', 'code': 'ADMIN'},
                {'name': 'Human Resources', 'code': 'HR'},
                {'name': 'Finance', 'code': 'FIN'},
            ]
            
            for dept_data in basic_departments:
                Department.objects.create(
                    organization=organization,
                    name=dept_data['name'],
                    code=dept_data['code'],
                    description=f'{dept_data["name"]} department'
                )
            
            messages.success(request, f'Organization "{org_name}" created successfully with basic departments!')
            return redirect('payroll_admin:organization_dashboard')
    
    context = {
        'title': 'Quick Setup Wizard',
        'organization_types': Organization.ORGANIZATION_TYPES
    }
    return render(request, 'admin/quick_setup_wizard.html', context)


def is_super_admin(user):
    """Check if user is a super admin"""
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='super_admin').exists())


@user_passes_test(is_super_admin)
def user_management_dashboard(request):
    """User management dashboard for super admins"""
    users = User.objects.all().order_by('username')
    roles = PayrollRoleManager.get_available_roles()

    # Get current organization
    current_org = Organization.objects.filter(is_active=True).first()

    # Get user roles
    user_roles = {}
    for user in users:
        user_roles[user.id] = PayrollRoleManager.get_user_role(user)

    context = {
        'users': users,
        'roles': roles,
        'user_roles': user_roles,
        'title': 'User Management',
        'organization': current_org,
        'current_org': current_org,
    }
    return render(request, 'admin/user_management.html', context)


@user_passes_test(is_super_admin)
def create_user(request):
    """Create a new user"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        password = request.POST.get('password')
        role = request.POST.get('role')

        # Validation
        if User.objects.filter(username=username).exists():
            messages.error(request, f'Username "{username}" already exists.')
            return redirect('payroll_admin:user_management')

        if User.objects.filter(email=email).exists():
            messages.error(request, f'Email "{email}" is already registered.')
            return redirect('payroll_admin:user_management')

        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Assign role
            if PayrollRoleManager.assign_user_role(user, role):
                messages.success(request, f'User "{username}" created successfully with role "{role.replace("_", " ").title()}".')
            else:
                messages.warning(request, f'User "{username}" created but role assignment failed.')

        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')

    return redirect('payroll_admin:user_management')


@user_passes_test(is_super_admin)
def edit_user_role(request, user_id):
    """Edit user role"""
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        new_role = request.POST.get('role')

        if PayrollRoleManager.assign_user_role(user, new_role):
            messages.success(request, f'Role updated for "{user.username}" to "{new_role.replace("_", " ").title()}".')
        else:
            messages.error(request, f'Failed to update role for "{user.username}".')

    return redirect('payroll_admin:user_management')


@user_passes_test(is_super_admin)
def toggle_user_status(request, user_id):
    """Toggle user active status"""
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()

        status = "activated" if user.is_active else "deactivated"
        messages.success(request, f'User "{user.username}" has been {status}.')

    return redirect('payroll_admin:user_management')


@user_passes_test(is_super_admin)
def delete_user(request, user_id):
    """Delete a user"""
    user = get_object_or_404(User, id=user_id)

    # Prevent deletion of current user
    if user == request.user:
        messages.error(request, 'You cannot delete your own account.')
        return redirect('payroll_admin:user_management')

    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'User "{username}" has been deleted.')

    return redirect('payroll_admin:user_management')


@user_passes_test(is_super_admin)
def initialize_roles(request):
    """Initialize default roles and permissions"""
    if request.method == 'POST':
        try:
            PayrollRoleManager.create_default_groups()
            messages.success(request, 'Default roles and permissions have been initialized successfully.')
        except Exception as e:
            messages.error(request, f'Error initializing roles: {str(e)}')

    return redirect('payroll_admin:user_management')
