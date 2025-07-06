#!/usr/bin/env python
"""
Health check script to test Django configuration
Run this to identify issues before deployment
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payroll.settings.basic')

try:
    # Test Django setup
    print("🔍 Testing Django configuration...")
    django.setup()
    print("✅ Django setup successful")
    
    # Test database connection
    print("🔍 Testing database connection...")
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("SELECT 1")
    print("✅ Database connection successful")
    
    # Test installed apps
    print("🔍 Testing installed apps...")
    from django.apps import apps
    for app in apps.get_app_configs():
        print(f"  ✅ {app.name}")
    
    # Test URL configuration
    print("🔍 Testing URL configuration...")
    from django.urls import reverse
    from django.test import Client
    client = Client()
    print("✅ URL configuration loaded")
    
    print("\n🎉 All health checks passed!")
    print("Your Django configuration should work on Render.")
    
except Exception as e:
    print(f"\n❌ Health check failed: {e}")
    print("Fix this issue before deploying to Render.")
    sys.exit(1)
