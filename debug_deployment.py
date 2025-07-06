#!/usr/bin/env python
"""
Debug script to test what's working in the deployment
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payroll.settings.sqlite')

# Setup Django
django.setup()

def test_deployment():
    print("🔍 Testing deployment configuration...")
    
    # Test 1: Check installed apps
    from django.conf import settings
    print(f"✅ Installed apps: {len(settings.INSTALLED_APPS)}")
    for app in settings.INSTALLED_APPS:
        print(f"  - {app}")
    
    # Test 2: Check URL patterns
    print("\n🔍 Testing URL patterns...")
    from django.urls import get_resolver
    resolver = get_resolver()
    print(f"✅ URL patterns loaded: {len(resolver.url_patterns)}")
    
    # Test 3: Check templates
    print("\n🔍 Testing templates...")
    template_dirs = settings.TEMPLATES[0]['DIRS']
    print(f"✅ Template directories: {template_dirs}")
    
    # Test 4: Check static files
    print("\n🔍 Testing static files...")
    print(f"✅ Static URL: {settings.STATIC_URL}")
    print(f"✅ Static root: {settings.STATIC_ROOT}")
    
    # Test 5: Test views
    print("\n🔍 Testing views...")
    try:
        from core.views import public_landing
        print("✅ public_landing view imported successfully")
    except Exception as e:
        print(f"❌ Error importing public_landing: {e}")
    
    try:
        from core.views import dashboard
        print("✅ dashboard view imported successfully")
    except Exception as e:
        print(f"❌ Error importing dashboard: {e}")
    
    print("\n🎯 Deployment test complete!")

if __name__ == "__main__":
    test_deployment()
