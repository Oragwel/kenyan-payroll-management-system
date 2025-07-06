#!/usr/bin/env python
"""
Test script to verify data preservation across deployments
"""

import os
import sys
import django
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payroll.settings.production')
django.setup()

def test_data_preservation():
    """Test if data is being preserved across deployments"""
    print("🔍 TESTING DATA PRESERVATION")
    print("=" * 50)
    
    try:
        from employees.models import Organization, Employee, Department, JobTitle
        from django.contrib.auth.models import User
        from statutory_deductions.models import SHIFRate, PAYETaxBand, NSSFRate
        
        # Check user data
        print("👥 USER DATA:")
        users = User.objects.all()
        print(f"   Total users: {users.count()}")
        for user in users:
            print(f"   - {user.username} (Active: {user.is_active}, Staff: {user.is_staff})")
        
        # Check organization data
        print("\n🏢 ORGANIZATION DATA:")
        orgs = Organization.objects.all()
        print(f"   Total organizations: {orgs.count()}")
        for org in orgs:
            print(f"   - {org.name} ({org.organization_type})")
            if org.address:
                print(f"     Address: {org.address}")
            if org.phone:
                print(f"     Phone: {org.phone}")
        
        # Check employee data
        print("\n👨‍💼 EMPLOYEE DATA:")
        employees = Employee.objects.all()
        print(f"   Total employees: {employees.count()}")
        for emp in employees[:5]:  # Show first 5
            print(f"   - {emp.first_name} {emp.last_name} ({emp.employment_type})")
        if employees.count() > 5:
            print(f"   ... and {employees.count() - 5} more employees")
        
        # Check department data
        print("\n🏛️ DEPARTMENT DATA:")
        departments = Department.objects.all()
        print(f"   Total departments: {departments.count()}")
        for dept in departments:
            print(f"   - {dept.name}")
        
        # Check job title data
        print("\n💼 JOB TITLE DATA:")
        job_titles = JobTitle.objects.all()
        print(f"   Total job titles: {job_titles.count()}")
        for title in job_titles:
            print(f"   - {title.title}")
        
        # Check tax data
        print("\n💰 TAX DATA:")
        shif_rates = SHIFRate.objects.filter(is_active=True)
        paye_bands = PAYETaxBand.objects.filter(is_active=True)
        nssf_rates = NSSFRate.objects.filter(is_active=True)
        
        print(f"   SHIF rates: {shif_rates.count()}")
        for rate in shif_rates:
            print(f"   - {rate.contribution_rate}% (Min: KES {rate.minimum_contribution})")
        
        print(f"   PAYE bands: {paye_bands.count()}")
        print(f"   NSSF rates: {nssf_rates.count()}")
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 DATA PRESERVATION SUMMARY:")
        
        total_data_items = (
            users.count() + orgs.count() + employees.count() + 
            departments.count() + job_titles.count()
        )
        
        if total_data_items > 0:
            print(f"✅ EXISTING DATA FOUND: {total_data_items} items")
            print("🛡️ This data should be PRESERVED during deployment")
            print("❌ If this data disappears after deployment, there's a bug!")
        else:
            print("ℹ️ NO EXISTING DATA FOUND")
            print("This appears to be a fresh installation")
        
        # Create test data marker
        if not Organization.objects.filter(name="TEST_DATA_PRESERVATION_MARKER").exists():
            print("\n🔬 Creating test data preservation marker...")
            test_org = Organization.objects.create(
                name="TEST_DATA_PRESERVATION_MARKER",
                organization_type="GOVERNMENT",
                address="Test Address for Data Preservation",
                phone="+254700000000",
                email="test@preservation.test"
            )
            print(f"✅ Created test marker: {test_org.name}")
            print("🔍 This marker should survive deployment!")
        else:
            marker = Organization.objects.get(name="TEST_DATA_PRESERVATION_MARKER")
            print(f"\n✅ TEST MARKER FOUND: {marker.name}")
            print("🎉 Data preservation is working!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing data preservation: {e}")
        return False

def main():
    print(f"🕒 Test run at: {datetime.now()}")
    success = test_data_preservation()
    
    if success:
        print("\n🎯 NEXT STEPS:")
        print("1. Note the data counts above")
        print("2. Deploy the system")
        print("3. Run this script again")
        print("4. Compare the data counts")
        print("5. All counts should be the same or higher (never lower)")
    
    return success

if __name__ == '__main__':
    main()
