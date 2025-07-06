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

def setup_tax_data():
    """Set up tax data including SHIF rates (only if missing)"""
    print("🔧 Checking tax data (PAYE, NSSF, SHIF, Housing Levy)...")

    try:
        from statutory_deductions.models import SHIFRate, PAYETaxBand, NSSFRate

        # Check if essential tax data already exists
        shif_exists = SHIFRate.objects.filter(is_active=True).exists()
        paye_exists = PAYETaxBand.objects.filter(is_active=True).exists()
        nssf_exists = NSSFRate.objects.filter(is_active=True).exists()

        if shif_exists and paye_exists and nssf_exists:
            print("✅ Tax data already exists - preserving existing data")
            return

        print("⚠️ Missing tax data detected - setting up required data...")
        from django.core.management import call_command
        call_command('setup_tax_data')
        print("✅ Tax data setup completed!")
    except Exception as e:
        print(f"⚠️ Tax data setup failed: {e}")
        print("This is not critical - system will still work")

def main():
    """Main function to create superuser and setup tax data"""
    print("🚀 Setting up Kenyan Payroll Management System...")

    # Create superuser
    create_superuser()

    # Setup tax data (including SHIF rates)
    setup_tax_data()

    print("✅ System setup completed!")

if __name__ == "__main__":
    main()
