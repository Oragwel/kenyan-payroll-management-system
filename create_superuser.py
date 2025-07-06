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
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payroll.settings.sqlite')

# Setup Django
django.setup()

from django.contrib.auth.models import User

def create_superuser():
    """Create superuser if it doesn't exist"""
    username = 'admin'
    email = 'admin@example.com'
    password = 'admin123'
    
    if User.objects.filter(username=username).exists():
        print(f"ℹ️ Superuser '{username}' already exists")
    else:
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"✅ Superuser '{username}' created successfully")
        print(f"   Username: {username}")
        print(f"   Password: {password}")

if __name__ == "__main__":
    create_superuser()
