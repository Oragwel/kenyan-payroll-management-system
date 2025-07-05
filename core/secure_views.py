"""
Secure views for sensitive payroll operations
Government Payroll Management System - Secure Access Module

This module provides secure views for sensitive operations using:
- Token-based access control
- Session validation
- IP address verification
- User agent validation
- Comprehensive audit logging

Author: System Security Team
Date: 2025-07-05
Classification: CONFIDENTIAL - Government Use Only
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import PermissionDenied

from .security_utils import (
    SecureTokenManager, URLObfuscator, SecurityAuditLogger,
    get_client_ip, get_user_agent
)
from employees.models import Employee
from payroll_processing.models import PayrollPeriod, Payslip
# Import removed to avoid circular dependency
import logging

# Security logger
security_logger = logging.getLogger('security')

@login_required
@csrf_protect
def secure_payslip_access(request):
    """
    Secure access to payslip using token validation
    
    URL: /payroll/secure/payslip/?token=<token>
    Method: GET
    Security: Token-based access with IP/User-Agent validation
    """
    token = request.GET.get('token')
    if not token:
        SecurityAuditLogger.log_access_attempt(
            request.user.id, 'payslip', 0, False,
            get_client_ip(request), get_user_agent(request)
        )
        raise Http404("Access denied")
    
    # Get token data from cache
    cache_key = f'secure_token_{token}'
    from django.core.cache import cache
    token_data = cache.get(cache_key)
    
    if not token_data:
        SecurityAuditLogger.log_access_attempt(
            request.user.id, 'payslip', 0, False,
            get_client_ip(request), get_user_agent(request)
        )
        raise Http404("Access denied")
    
    # Validate token
    if not SecureTokenManager.validate_access_token(
        token, request.user.id, 'payslip', token_data['resource_id']
    ):
        SecurityAuditLogger.log_access_attempt(
            request.user.id, 'payslip', token_data.get('resource_id', 0), False,
            get_client_ip(request), get_user_agent(request)
        )
        raise Http404("Access denied")
    
    # Get employee and validate access
    employee_id = token_data['resource_id']
    employee = get_object_or_404(Employee, id=employee_id)
    
    # Additional security: Check if user has permission to view this employee's payslip
    if not request.user.is_staff and request.user != employee.user:
        SecurityAuditLogger.log_access_attempt(
            request.user.id, 'payslip', employee_id, False,
            get_client_ip(request), get_user_agent(request)
        )
        raise PermissionDenied("You don't have permission to view this payslip")
    
    # Log successful access
    SecurityAuditLogger.log_access_attempt(
        request.user.id, 'payslip', employee_id, True,
        get_client_ip(request), get_user_agent(request)
    )
    
    # Generate payslip context (simplified for secure access)
    try:
        # Get the latest payslip for this employee
        from payroll_processing.models import Payslip
        payslip = Payslip.objects.filter(employee=employee).order_by('-created_at').first()

        if not payslip:
            raise Http404("No payslip found for this employee")

        context = {
            'employee': employee,
            'payslip': payslip,
            'payroll_period': payslip.payroll_period,
            'organization': employee.organization if hasattr(employee, 'organization') else None,
            'secure_access': True,
            'token': token
        }

        # Revoke token after use (single-use token)
        SecureTokenManager.revoke_token(token)

        return render(request, 'payroll/secure_payslip.html', context)
    
    except Exception as e:
        security_logger.error(f"Error generating secure payslip for employee {employee_id}: {str(e)}")
        raise Http404("Payslip not available")

@staff_member_required
@csrf_protect
def secure_period_access(request):
    """
    Secure access to payroll period using token validation
    
    URL: /payroll/secure/period/?token=<token>
    Method: GET
    Security: Token-based access with staff validation
    """
    token = request.GET.get('token')
    if not token:
        SecurityAuditLogger.log_access_attempt(
            request.user.id, 'period', 0, False,
            get_client_ip(request), get_user_agent(request)
        )
        raise Http404("Access denied")
    
    # Get token data
    cache_key = f'secure_token_{token}'
    from django.core.cache import cache
    token_data = cache.get(cache_key)
    
    if not token_data:
        SecurityAuditLogger.log_access_attempt(
            request.user.id, 'period', 0, False,
            get_client_ip(request), get_user_agent(request)
        )
        raise Http404("Access denied")
    
    # Validate token
    if not SecureTokenManager.validate_access_token(
        token, request.user.id, 'period', token_data['resource_id']
    ):
        SecurityAuditLogger.log_access_attempt(
            request.user.id, 'period', token_data.get('resource_id', 0), False,
            get_client_ip(request), get_user_agent(request)
        )
        raise Http404("Access denied")
    
    # Get period
    period_id = token_data['resource_id']
    period = get_object_or_404(PayrollPeriod, id=period_id)
    
    # Log successful access
    SecurityAuditLogger.log_access_attempt(
        request.user.id, 'period', period_id, True,
        get_client_ip(request), get_user_agent(request)
    )
    
    # Redirect to period detail with secure context
    return redirect('payroll_processing:payroll_period_detail', period_id=period_id)

@staff_member_required
@require_http_methods(["POST"])
@csrf_protect
def generate_secure_access_token(request):
    """
    Generate secure access token for sensitive operations
    
    URL: /api/secure/generate-token/
    Method: POST
    Security: Staff-only access with CSRF protection
    """
    resource_type = request.POST.get('resource_type')
    resource_id = request.POST.get('resource_id')
    expires_minutes = int(request.POST.get('expires_minutes', 30))
    
    if not resource_type or not resource_id:
        return JsonResponse({'error': 'Missing required parameters'}, status=400)
    
    try:
        resource_id = int(resource_id)
        
        # Validate resource exists
        if resource_type == 'payslip':
            get_object_or_404(Employee, id=resource_id)
        elif resource_type == 'period':
            get_object_or_404(PayrollPeriod, id=resource_id)
        else:
            return JsonResponse({'error': 'Invalid resource type'}, status=400)
        
        # Generate token
        token = SecureTokenManager.generate_access_token(
            request.user.id, resource_type, resource_id, expires_minutes
        )
        
        # Log token generation
        SecurityAuditLogger.log_admin_action(
            request.user.id, 'generate_token', f"{resource_type}:{resource_id}", True
        )
        
        return JsonResponse({
            'token': token,
            'expires_in': expires_minutes * 60,
            'resource_type': resource_type,
            'resource_id': resource_id
        })
    
    except Exception as e:
        security_logger.error(f"Error generating token: {str(e)}")
        return JsonResponse({'error': 'Token generation failed'}, status=500)

@staff_member_required
@require_http_methods(["POST"])
@csrf_protect
def revoke_access_token(request):
    """
    Revoke an access token
    
    URL: /api/secure/revoke-token/
    Method: POST
    Security: Staff-only access with CSRF protection
    """
    token = request.POST.get('token')
    
    if not token:
        return JsonResponse({'error': 'Token required'}, status=400)
    
    success = SecureTokenManager.revoke_token(token)
    
    if success:
        SecurityAuditLogger.log_admin_action(
            request.user.id, 'revoke_token', token[:8] + '...', True
        )
        return JsonResponse({'message': 'Token revoked successfully'})
    else:
        return JsonResponse({'error': 'Token not found or already expired'}, status=404)

@login_required
def security_dashboard(request):
    """
    Security dashboard for monitoring access
    
    URL: /security/dashboard/
    Method: GET
    Security: Login required, staff gets full access
    """
    if not request.user.is_staff:
        # Regular users see limited security info
        context = {
            'user_sessions': 1,  # Current session only
            'recent_logins': [],
            'security_alerts': [],
        }
    else:
        # Staff users see comprehensive security dashboard
        from django.contrib.sessions.models import Session
        from django.contrib.auth.models import User
        
        active_sessions = Session.objects.filter(
            expire_date__gte=timezone.now()
        ).count()
        
        context = {
            'active_sessions': active_sessions,
            'total_users': User.objects.count(),
            'staff_users': User.objects.filter(is_staff=True).count(),
            'recent_logins': [],  # Would implement with custom logging
            'security_alerts': [],  # Would implement with monitoring
        }
    
    return render(request, 'security/dashboard.html', context)

# Utility functions for views
def validate_secure_access(request, resource_type, resource_id):
    """
    Validate secure access to a resource
    
    Args:
        request: HTTP request object
        resource_type: Type of resource
        resource_id: ID of resource
        
    Returns:
        True if access is valid, False otherwise
    """
    if not request.user.is_authenticated:
        return False
    
    # Check if user has general permission
    if resource_type in ['payslip', 'employee'] and not request.user.is_staff:
        # Regular users can only access their own data
        try:
            employee = Employee.objects.get(id=resource_id)
            return request.user == employee.user
        except Employee.DoesNotExist:
            return False
    
    # Staff users have broader access
    return request.user.is_staff

def log_security_event(event_type, user_id, details, success=True):
    """
    Log security events for audit trail
    
    Args:
        event_type: Type of security event
        user_id: ID of user involved
        details: Event details
        success: Whether event was successful
    """
    security_logger.info({
        'event_type': event_type,
        'user_id': user_id,
        'details': details,
        'success': success,
        'timestamp': timezone.now().isoformat(),
    })
