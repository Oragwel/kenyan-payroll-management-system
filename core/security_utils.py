"""
Security utilities for URL obfuscation and access control
Government Payroll Management System - Security Module

This module provides security utilities for:
- URL obfuscation using UUIDs and tokens
- Session-based access control
- Secure route generation
- Access token management

Author: System Security Team
Date: 2025-07-05
Classification: CONFIDENTIAL - Government Use Only
"""

import uuid
import secrets
import hashlib
from datetime import datetime, timedelta
from django.core.cache import cache
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from typing import Dict, Optional, Any
import logging

# Security logger
security_logger = logging.getLogger('security')

class SecureTokenManager:
    """
    Manages secure tokens for sensitive operations
    """
    
    @staticmethod
    def generate_access_token(user_id: int, resource_type: str, resource_id: int, 
                            expires_minutes: int = 30) -> str:
        """
        Generate a secure access token for sensitive resources
        
        Args:
            user_id: ID of the user requesting access
            resource_type: Type of resource (e.g., 'payslip', 'employee', 'period')
            resource_id: ID of the specific resource
            expires_minutes: Token expiration time in minutes
            
        Returns:
            Secure token string
        """
        token = secrets.token_urlsafe(32)
        
        token_data = {
            'user_id': user_id,
            'resource_type': resource_type,
            'resource_id': resource_id,
            'created_at': timezone.now().isoformat(),
            'expires_at': (timezone.now() + timedelta(minutes=expires_minutes)).isoformat(),
            'ip_address': None,  # To be set by view
            'user_agent': None,  # To be set by view
        }
        
        cache_key = f'secure_token_{token}'
        cache.set(cache_key, token_data, timeout=expires_minutes * 60)
        
        # Log token generation
        security_logger.info(f"Access token generated for user {user_id}, resource {resource_type}:{resource_id}")
        
        return token
    
    @staticmethod
    def validate_access_token(token: str, user_id: int, resource_type: str, 
                            resource_id: int) -> bool:
        """
        Validate an access token
        
        Args:
            token: Token to validate
            user_id: Current user ID
            resource_type: Expected resource type
            resource_id: Expected resource ID
            
        Returns:
            True if token is valid, False otherwise
        """
        cache_key = f'secure_token_{token}'
        token_data = cache.get(cache_key)
        
        if not token_data:
            security_logger.warning(f"Invalid or expired token used by user {user_id}")
            return False
        
        # Validate token data
        if (token_data['user_id'] != user_id or 
            token_data['resource_type'] != resource_type or 
            token_data['resource_id'] != resource_id):
            security_logger.warning(f"Token validation failed for user {user_id}")
            return False
        
        # Check expiration
        expires_at = datetime.fromisoformat(token_data['expires_at'].replace('Z', '+00:00'))
        if timezone.now() > expires_at:
            security_logger.warning(f"Expired token used by user {user_id}")
            cache.delete(cache_key)
            return False
        
        return True
    
    @staticmethod
    def revoke_token(token: str) -> bool:
        """
        Revoke an access token
        
        Args:
            token: Token to revoke
            
        Returns:
            True if token was revoked, False if not found
        """
        cache_key = f'secure_token_{token}'
        if cache.get(cache_key):
            cache.delete(cache_key)
            security_logger.info(f"Token {token[:8]}... revoked")
            return True
        return False

class URLObfuscator:
    """
    Handles URL obfuscation for sensitive routes
    """
    
    @staticmethod
    def generate_uuid_for_model(model_instance) -> str:
        """
        Generate a UUID for a model instance
        
        Args:
            model_instance: Django model instance
            
        Returns:
            UUID string
        """
        if hasattr(model_instance, 'uuid') and model_instance.uuid:
            return str(model_instance.uuid)
        
        # Generate new UUID if not exists
        new_uuid = uuid.uuid4()
        if hasattr(model_instance, 'uuid'):
            model_instance.uuid = new_uuid
            model_instance.save(update_fields=['uuid'])
        
        return str(new_uuid)
    
    @staticmethod
    def obfuscate_id(model_id: int, salt: str = None) -> str:
        """
        Obfuscate a model ID using hashing
        
        Args:
            model_id: ID to obfuscate
            salt: Optional salt for hashing
            
        Returns:
            Obfuscated ID string
        """
        if not salt:
            salt = getattr(settings, 'SECRET_KEY', 'default_salt')
        
        # Create hash of ID + salt
        hash_input = f"{model_id}:{salt}".encode('utf-8')
        hash_object = hashlib.sha256(hash_input)
        
        # Return first 16 characters of hash
        return hash_object.hexdigest()[:16]
    
    @staticmethod
    def deobfuscate_id(obfuscated_id: str, max_id: int = 10000, salt: str = None) -> Optional[int]:
        """
        Deobfuscate an ID by trying all possibilities (brute force)
        
        Args:
            obfuscated_id: Obfuscated ID to decode
            max_id: Maximum ID to try
            salt: Salt used for obfuscation
            
        Returns:
            Original ID if found, None otherwise
        """
        if not salt:
            salt = getattr(settings, 'SECRET_KEY', 'default_salt')
        
        for test_id in range(1, max_id + 1):
            if URLObfuscator.obfuscate_id(test_id, salt) == obfuscated_id:
                return test_id
        
        return None

class SecureRouteGenerator:
    """
    Generates secure routes for sensitive operations
    """
    
    @staticmethod
    def generate_payslip_url(employee_id: int, user: User) -> str:
        """
        Generate secure URL for payslip access
        
        Args:
            employee_id: Employee ID
            user: Current user
            
        Returns:
            Secure URL with token
        """
        token = SecureTokenManager.generate_access_token(
            user.id, 'payslip', employee_id, expires_minutes=30
        )
        return f"/payroll/secure/payslip/?token={token}"
    
    @staticmethod
    def generate_period_url(period_id: int, user: User) -> str:
        """
        Generate secure URL for period access
        
        Args:
            period_id: Period ID
            user: Current user
            
        Returns:
            Secure URL with token
        """
        token = SecureTokenManager.generate_access_token(
            user.id, 'period', period_id, expires_minutes=60
        )
        return f"/payroll/secure/period/?token={token}"

class SecurityAuditLogger:
    """
    Logs security-related events
    """
    
    @staticmethod
    def log_access_attempt(user_id: int, resource_type: str, resource_id: int, 
                          success: bool, ip_address: str = None, user_agent: str = None):
        """
        Log access attempt to sensitive resource
        """
        log_data = {
            'user_id': user_id,
            'resource_type': resource_type,
            'resource_id': resource_id,
            'success': success,
            'timestamp': timezone.now().isoformat(),
            'ip_address': ip_address,
            'user_agent': user_agent,
        }
        
        if success:
            security_logger.info(f"Successful access: {log_data}")
        else:
            security_logger.warning(f"Failed access attempt: {log_data}")
    
    @staticmethod
    def log_admin_action(user_id: int, action: str, target: str, success: bool):
        """
        Log administrative actions
        """
        log_data = {
            'user_id': user_id,
            'action': action,
            'target': target,
            'success': success,
            'timestamp': timezone.now().isoformat(),
        }
        
        security_logger.info(f"Admin action: {log_data}")

# Security decorators and middleware helpers
def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_user_agent(request):
    """Get user agent from request"""
    return request.META.get('HTTP_USER_AGENT', '')
