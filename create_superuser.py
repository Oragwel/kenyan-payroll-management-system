#!/usr/bin/env python
"""
Create superuser script for Render deployment
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payroll.settings.production')

# Setup Django
django.setup()

from django.contrib.auth.models import User

def create_superuser():
    """Create superuser if it doesn't exist"""
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

    print(f"🔍 Checking for superuser '{username}'...")

    # Check if user exists
    existing_user = User.objects.filter(username=username).first()
    if existing_user:
        print(f"ℹ️ Superuser '{username}' already exists")
        print(f"   Email: {existing_user.email}")
        print(f"   Is active: {existing_user.is_active}")
        print(f"   Is superuser: {existing_user.is_superuser}")

        # Update password to ensure it matches
        existing_user.set_password(password)
        existing_user.save()
        print(f"🔄 Updated password for existing superuser")
    else:
        # Create new superuser
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"✅ Superuser '{username}' created successfully")
        print(f"   Username: {username}")
        print(f"   Email: {email}")
        print(f"   Password: {password}")

    # Verify the user can authenticate
    from django.contrib.auth import authenticate
    auth_user = authenticate(username=username, password=password)
    if auth_user:
        print(f"✅ Authentication test successful for '{username}'")
    else:
        print(f"❌ Authentication test failed for '{username}'")

if __name__ == "__main__":
    create_superuser()
