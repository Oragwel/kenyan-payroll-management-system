from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from .models import Employee, Department, Organization


class PayrollRoleManager:
    """Manage user roles and permissions for the payroll system"""
    
    # Define role permissions
    ROLE_PERMISSIONS = {
        'super_admin': {
            'description': 'Full system access - can manage everything',
            'permissions': [
                # User management
                'auth.add_user', 'auth.change_user', 'auth.delete_user', 'auth.view_user',
                'auth.add_group', 'auth.change_group', 'auth.delete_group', 'auth.view_group',
                
                # Organization management
                'employees.add_organization', 'employees.change_organization', 
                'employees.delete_organization', 'employees.view_organization',
                
                # Employee management
                'employees.add_employee', 'employees.change_employee', 
                'employees.delete_employee', 'employees.view_employee',
                
                # Department management
                'employees.add_department', 'employees.change_department', 
                'employees.delete_department', 'employees.view_department',
                
                # Job title management
                'employees.add_jobtitle', 'employees.change_jobtitle', 
                'employees.delete_jobtitle', 'employees.view_jobtitle',
                
                # Salary structure management
                'employees.add_salarystructure', 'employees.change_salarystructure', 
                'employees.delete_salarystructure', 'employees.view_salarystructure',
                
                # Payroll management
                'payroll_processing.add_payslip', 'payroll_processing.change_payslip', 
                'payroll_processing.delete_payslip', 'payroll_processing.view_payslip',
                'payroll_processing.add_payrollperiod', 'payroll_processing.change_payrollperiod', 
                'payroll_processing.delete_payrollperiod', 'payroll_processing.view_payrollperiod',
                
                # Statutory deductions
                'statutory_deductions.add_nssfcontribution', 'statutory_deductions.change_nssfcontribution',
                'statutory_deductions.view_nssfcontribution', 'statutory_deductions.add_shifcontribution',
                'statutory_deductions.change_shifcontribution', 'statutory_deductions.view_shifcontribution',
                'statutory_deductions.add_payededuction', 'statutory_deductions.change_payededuction',
                'statutory_deductions.view_payededuction',
            ]
        },
        
        'admin': {
            'description': 'Organization administrator - can manage employees and payroll',
            'permissions': [
                # Employee management
                'employees.add_employee', 'employees.change_employee', 'employees.view_employee',
                'employees.view_organization', 'employees.view_department',
                
                # Job title management
                'employees.add_jobtitle', 'employees.change_jobtitle', 'employees.view_jobtitle',
                
                # Salary structure management
                'employees.add_salarystructure', 'employees.change_salarystructure', 
                'employees.view_salarystructure',
                
                # Payroll management
                'payroll_processing.add_payslip', 'payroll_processing.change_payslip', 
                'payroll_processing.view_payslip', 'payroll_processing.view_payrollperiod',
                
                # Statutory deductions (view only)
                'statutory_deductions.view_nssfcontribution', 'statutory_deductions.view_shifcontribution',
                'statutory_deductions.view_payededuction',
            ]
        },
        
        'hr_manager': {
            'description': 'HR Manager - can manage employees and view payroll',
            'permissions': [
                # Employee management
                'employees.add_employee', 'employees.change_employee', 'employees.view_employee',
                'employees.view_organization', 'employees.view_department',
                
                # Job title management
                'employees.add_jobtitle', 'employees.change_jobtitle', 'employees.view_jobtitle',
                
                # Payroll viewing
                'payroll_processing.view_payslip', 'payroll_processing.view_payrollperiod',
                
                # Statutory deductions (view only)
                'statutory_deductions.view_nssfcontribution', 'statutory_deductions.view_shifcontribution',
                'statutory_deductions.view_payededuction',
            ]
        },
        
        'payroll_officer': {
            'description': 'Payroll Officer - can process payroll and manage salary structures',
            'permissions': [
                # Employee viewing
                'employees.view_employee', 'employees.view_organization', 'employees.view_department',
                
                # Salary structure management
                'employees.add_salarystructure', 'employees.change_salarystructure', 
                'employees.view_salarystructure',
                
                # Payroll management
                'payroll_processing.add_payslip', 'payroll_processing.change_payslip', 
                'payroll_processing.view_payslip', 'payroll_processing.add_payrollperiod',
                'payroll_processing.change_payrollperiod', 'payroll_processing.view_payrollperiod',
                
                # Statutory deductions
                'statutory_deductions.add_nssfcontribution', 'statutory_deductions.change_nssfcontribution',
                'statutory_deductions.view_nssfcontribution', 'statutory_deductions.add_shifcontribution',
                'statutory_deductions.change_shifcontribution', 'statutory_deductions.view_shifcontribution',
                'statutory_deductions.add_payededuction', 'statutory_deductions.change_payededuction',
                'statutory_deductions.view_payededuction',
            ]
        },
        
        'employee': {
            'description': 'Employee - can view own payroll information',
            'permissions': [
                # Limited employee viewing (own record only)
                'employees.view_employee',
                
                # Limited payroll viewing (own payslips only)
                'payroll_processing.view_payslip',
            ]
        },
        
        'viewer': {
            'description': 'Read-only access to reports and data',
            'permissions': [
                # View-only permissions
                'employees.view_employee', 'employees.view_organization', 'employees.view_department',
                'employees.view_jobtitle', 'employees.view_salarystructure',
                'payroll_processing.view_payslip', 'payroll_processing.view_payrollperiod',
                'statutory_deductions.view_nssfcontribution', 'statutory_deductions.view_shifcontribution',
                'statutory_deductions.view_payededuction',
            ]
        }
    }
    
    @classmethod
    def create_default_groups(cls):
        """Create default user groups with permissions"""
        with transaction.atomic():
            for role_name, role_data in cls.ROLE_PERMISSIONS.items():
                group, created = Group.objects.get_or_create(
                    name=role_name,
                    defaults={'name': role_name}
                )
                
                if created:
                    print(f"Created group: {role_name}")
                
                # Clear existing permissions
                group.permissions.clear()
                
                # Add permissions to group
                for perm_codename in role_data['permissions']:
                    try:
                        app_label, codename = perm_codename.split('.')
                        permission = Permission.objects.get(
                            content_type__app_label=app_label,
                            codename=codename
                        )
                        group.permissions.add(permission)
                    except Permission.DoesNotExist:
                        print(f"Permission not found: {perm_codename}")
                    except ValueError:
                        print(f"Invalid permission format: {perm_codename}")
                
                print(f"Updated permissions for group: {role_name}")
    
    @classmethod
    def assign_user_role(cls, user, role_name):
        """Assign a role to a user"""
        if role_name not in cls.ROLE_PERMISSIONS:
            raise ValueError(f"Invalid role: {role_name}")
        
        # Remove user from all payroll-related groups
        for group_name in cls.ROLE_PERMISSIONS.keys():
            try:
                group = Group.objects.get(name=group_name)
                user.groups.remove(group)
            except Group.DoesNotExist:
                pass
        
        # Add user to the specified group
        try:
            group = Group.objects.get(name=role_name)
            user.groups.add(group)
            
            # Set staff status based on role
            if role_name in ['super_admin', 'admin']:
                user.is_staff = True
                if role_name == 'super_admin':
                    user.is_superuser = True
            else:
                user.is_staff = False
                user.is_superuser = False
            
            user.save()
            return True
        except Group.DoesNotExist:
            return False
    
    @classmethod
    def get_user_role(cls, user):
        """Get the primary role of a user"""
        for role_name in cls.ROLE_PERMISSIONS.keys():
            if user.groups.filter(name=role_name).exists():
                return role_name
        return None
    
    @classmethod
    def get_available_roles(cls):
        """Get list of available roles with descriptions"""
        return [
            {
                'name': role_name,
                'display_name': role_name.replace('_', ' ').title(),
                'description': role_data['description']
            }
            for role_name, role_data in cls.ROLE_PERMISSIONS.items()
        ]
    
    @classmethod
    def create_super_admin(cls, username, email, password, first_name='', last_name=''):
        """Create a super admin user"""
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            is_superuser=True
        )
        
        cls.assign_user_role(user, 'super_admin')
        return user
