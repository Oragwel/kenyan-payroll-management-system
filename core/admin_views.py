from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from employees.models import Employee, Department, Organization
from payroll_processing.models import Payslip, PayrollPeriod


@staff_member_required
def admin_dashboard(request):
    """Enhanced admin dashboard for payroll system"""
    
    # Get current organization
    current_org = Organization.objects.filter(is_active=True).first()
    
    # Basic statistics
    total_employees = Employee.objects.filter(is_active=True).count()
    total_departments = Department.objects.count()
    total_organizations = Organization.objects.count()
    
    # Employee statistics by type
    employee_stats = Employee.objects.filter(is_active=True).values('employment_type').annotate(
        count=Count('id')
    ).order_by('employment_type')
    
    # Recent payroll records (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_payrolls = Payslip.objects.filter(
        created_at__gte=thirty_days_ago
    ).select_related('employee', 'employee__department').order_by('-created_at')[:10]

    # Monthly payroll summary
    current_month = timezone.now().replace(day=1)
    monthly_payroll = Payslip.objects.filter(
        payroll_period__start_date__gte=current_month
    ).aggregate(
        total_gross=Sum('basic_salary'),
        total_net=Sum('net_pay'),
        total_deductions=Sum('total_deductions'),
        count=Count('id')
    )
    
    # Department statistics
    dept_stats = Department.objects.annotate(
        employee_count=Count('employee', filter=Q(employee__is_active=True))
    ).order_by('-employee_count')[:5]
    
    # Recent employees (last 7 days)
    week_ago = timezone.now() - timedelta(days=7)
    recent_employees = Employee.objects.filter(
        created_at__gte=week_ago
    ).select_related('department').order_by('-created_at')[:5]
    
    # System alerts
    alerts = []
    
    # Check for employees without payroll records
    employees_without_payroll = Employee.objects.filter(
        is_active=True,
        payslips__isnull=True
    ).count()
    if employees_without_payroll > 0:
        alerts.append({
            'type': 'warning',
            'message': f'{employees_without_payroll} active employees have no payroll records',
            'action_url': '/employees/',
            'action_text': 'View Employees'
        })
    
    # Check for missing organization setup
    if not current_org:
        alerts.append({
            'type': 'danger',
            'message': 'No default organization set. Please configure your organization.',
            'action_url': '/admin/payroll/organizations/',
            'action_text': 'Setup Organization'
        })
    
    # Check for departments without employees
    empty_departments = Department.objects.annotate(
        emp_count=Count('employee', filter=Q(employee__is_active=True))
    ).filter(emp_count=0).count()
    if empty_departments > 0:
        alerts.append({
            'type': 'info',
            'message': f'{empty_departments} departments have no active employees',
            'action_url': '/admin/employees/department/',
            'action_text': 'Manage Departments'
        })
    
    context = {
        'title': 'Payroll System Dashboard',
        'current_org': current_org,
        'total_employees': total_employees,
        'total_departments': total_departments,
        'total_organizations': total_organizations,
        'employee_stats': employee_stats,
        'recent_payrolls': recent_payrolls,
        'monthly_payroll': monthly_payroll,
        'dept_stats': dept_stats,
        'recent_employees': recent_employees,
        'alerts': alerts,
        'current_month': current_month.strftime('%B %Y'),
    }
    
    return render(request, 'admin/payroll_dashboard.html', context)


@staff_member_required
def admin_reports(request):
    """Admin reports overview"""
    # Get current organization
    current_org = Organization.objects.filter(is_active=True).first()

    # Get key metrics for the dashboard
    total_employees = Employee.objects.count()
    active_payroll_periods = PayrollPeriod.objects.filter(
        status__in=['PROCESSING', 'COMPLETED', 'APPROVED']
    ).count()
    total_departments = Department.objects.count()
    total_payslips = Payslip.objects.count()

    context = {
        'title': 'Reports & Analytics',
        'organization': current_org,
        'current_org': current_org,
        'total_employees': total_employees,
        'active_payroll_periods': active_payroll_periods,
        'total_departments': total_departments,
        'total_payslips': total_payslips,
    }
    return render(request, 'admin/reports_dashboard.html', context)


@staff_member_required
def admin_settings(request):
    """Admin system settings"""
    current_org = Organization.objects.filter(is_active=True).first()
    all_orgs = Organization.objects.all().order_by('name')
    
    context = {
        'title': 'System Settings',
        'current_org': current_org,
        'all_orgs': all_orgs,
    }
    return render(request, 'admin/settings_dashboard.html', context)


@login_required
def admin_redirect(request):
    """Redirect admin users to the enhanced dashboard"""
    if request.user.is_staff:
        return redirect('core:admin_dashboard')
    else:
        return redirect('dashboard')
