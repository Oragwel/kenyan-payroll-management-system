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

def check_data_preservation():
    """Check if existing data is being preserved"""
    print("🔍 Checking data preservation...")

    try:
        from employees.models import Organization, Employee
        from django.contrib.auth.models import User

        # Check existing data
        org_count = Organization.objects.count()
        emp_count = Employee.objects.count()
        user_count = User.objects.count()

        print(f"📊 Current data status:")
        print(f"   - Organizations: {org_count}")
        print(f"   - Employees: {emp_count}")
        print(f"   - Users: {user_count}")

        if org_count > 0 or emp_count > 0:
            print("✅ Existing data detected - will preserve all data")
            return True
        else:
            print("ℹ️ No existing data found - fresh installation")
            return False

    except Exception as e:
        print(f"⚠️ Data check failed: {e}")
        return False

def setup_tax_data():
    """Set up tax data including SHIF rates (only if missing)"""
    print("🔧 Checking tax data (PAYE, NSSF, SHIF, Housing Levy)...")

    try:
        from statutory_deductions.models import SHIFRate, PAYETaxBand, NSSFRate

        # Check if essential tax data already exists
        shif_exists = SHIFRate.objects.filter(is_active=True).exists()
        paye_exists = PAYETaxBand.objects.filter(is_active=True).exists()
        nssf_exists = NSSFRate.objects.filter(is_active=True).exists()

        print(f"   - SHIF rates: {'✅ Found' if shif_exists else '❌ Missing'}")
        print(f"   - PAYE bands: {'✅ Found' if paye_exists else '❌ Missing'}")
        print(f"   - NSSF rates: {'✅ Found' if nssf_exists else '❌ Missing'}")

        if shif_exists and paye_exists and nssf_exists:
            print("✅ All tax data exists - preserving existing data")
            return

        print("⚠️ Missing tax data detected - setting up required data...")
        print("🔒 IMPORTANT: This will NOT affect existing organization or employee data")

        from django.core.management import call_command
        call_command('setup_tax_data')
        print("✅ Tax data setup completed!")
    except Exception as e:
        print(f"⚠️ Tax data setup failed: {e}")
        print("This is not critical - system will still work")

def main():
    """Main function to create superuser and setup tax data"""
    print("🚀 Setting up Kenyan Payroll Management System...")
    print("🔒 DATA PRESERVATION MODE: Existing data will NOT be deleted")

    # Check data preservation status
    has_existing_data = check_data_preservation()

    if has_existing_data:
        print("🛡️ EXISTING DATA DETECTED - Operating in preservation mode")
        print("   - Will NOT delete organizations")
        print("   - Will NOT delete employees")
        print("   - Will NOT reset settings")
        print("   - Will only add missing system data")

    # Create superuser (only if doesn't exist)
    create_superuser()

    # Setup tax data (only if missing)
    setup_tax_data()

    if has_existing_data:
        print("✅ System updated while preserving ALL existing data!")
    else:
        print("✅ Fresh system setup completed!")

if __name__ == "__main__":
    main()
