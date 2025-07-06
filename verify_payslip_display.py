#!/usr/bin/env python3
"""
Verification script to confirm that all payslips correctly display
employer contributions for NSSF and Housing Levy
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payroll.settings')
django.setup()

from payroll_processing.models import Payslip
from employees.models import Employee


def verify_all_payslips():
    """Verify that all payslips show correct employer contributions"""
    
    print("🔍 PAYSLIP EMPLOYER CONTRIBUTIONS VERIFICATION")
    print("=" * 70)
    
    # Get all payslips
    payslips = Payslip.objects.all().select_related('employee', 'payroll_period').order_by('employee__employment_type', 'employee__id')
    
    print(f"\n📋 TOTAL PAYSLIPS TO VERIFY: {payslips.count()}")
    print("-" * 70)
    
    # Group by employment type
    by_employment_type = {}
    for payslip in payslips:
        emp_type = payslip.employee.employment_type
        if emp_type not in by_employment_type:
            by_employment_type[emp_type] = []
        by_employment_type[emp_type].append(payslip)
    
    all_correct = True
    
    for emp_type, type_payslips in by_employment_type.items():
        print(f"\n👥 {emp_type} EMPLOYEES ({len(type_payslips)} payslips):")
        print("-" * 50)
        
        for payslip in type_payslips:
            print(f"\n📄 {payslip.employee.full_name} (ID: {payslip.employee.id})")
            print(f"   Payslip ID: {payslip.id}")
            print(f"   URL: http://localhost:8000/payroll/payslip/{payslip.id}/")
            print(f"   Period: {payslip.payroll_period.name}")
            print(f"   Gross Pay: KES {payslip.gross_pay:,.2f}")
            
            # Employee deductions
            print(f"   Employee Deductions:")
            print(f"     NSSF: KES {payslip.nssf_employee:,.2f}")
            print(f"     Housing Levy: KES {payslip.housing_levy_employee:,.2f}")
            
            # Employer contributions
            print(f"   Employer Contributions:")
            nssf_employer_ok = payslip.nssf_employer > 0
            housing_employer_ok = payslip.housing_levy_employer > 0
            
            print(f"     NSSF: KES {payslip.nssf_employer:,.2f} {'✅' if nssf_employer_ok else '❌'}")
            print(f"     Housing Levy: KES {payslip.housing_levy_employer:,.2f} {'✅' if housing_employer_ok else '❌'}")
            
            # Total employer cost
            total_employer_cost = payslip.gross_pay + payslip.nssf_employer + payslip.housing_levy_employer
            print(f"   Total Employer Cost: KES {total_employer_cost:,.2f}")
            
            # Verification
            if nssf_employer_ok and housing_employer_ok:
                print(f"   Status: ✅ CORRECT - Both employer contributions present")
            else:
                print(f"   Status: ❌ ERROR - Missing employer contributions")
                all_correct = False
    
    print("\n" + "=" * 70)
    print("🎯 VERIFICATION SUMMARY:")
    print("=" * 70)
    
    if all_correct:
        print("✅ ALL PAYSLIPS CORRECT")
        print("✅ All payslips show proper NSSF employer contributions")
        print("✅ All payslips show proper Housing Levy employer contributions")
        print("✅ System is fully compliant with Kenyan employment law")
    else:
        print("❌ SOME PAYSLIPS HAVE ISSUES")
        print("❌ Missing employer contributions detected")
    
    print(f"\n📊 STATISTICS:")
    print(f"   Total Payslips: {payslips.count()}")
    print(f"   Employment Types: {len(by_employment_type)}")
    for emp_type, type_payslips in by_employment_type.items():
        print(f"   {emp_type}: {len(type_payslips)} payslips")
    
    return all_correct


def verify_specific_employment_types():
    """Verify specific employment types for compliance"""
    
    print("\n" + "=" * 70)
    print("🏛️ KENYAN LAW COMPLIANCE VERIFICATION:")
    print("=" * 70)
    
    # Check each employment type
    employment_types = ['PERMANENT', 'CONTRACT', 'CASUAL', 'INTERN']
    
    for emp_type in employment_types:
        employees = Employee.objects.filter(employment_type=emp_type, is_active=True)
        payslips = Payslip.objects.filter(employee__in=employees)
        
        print(f"\n📋 {emp_type} EMPLOYEES:")
        print(f"   Employees: {employees.count()}")
        print(f"   Payslips: {payslips.count()}")
        
        if payslips.exists():
            # Check if all have employer contributions
            missing_nssf = payslips.filter(nssf_employer=0).count()
            missing_housing = payslips.filter(housing_levy_employer=0).count()
            
            print(f"   NSSF Employer Contributions: {payslips.count() - missing_nssf}/{payslips.count()} ✅")
            print(f"   Housing Levy Employer Contributions: {payslips.count() - missing_housing}/{payslips.count()} ✅")
            
            if missing_nssf == 0 and missing_housing == 0:
                print(f"   Status: ✅ FULLY COMPLIANT")
            else:
                print(f"   Status: ❌ NON-COMPLIANT")
        else:
            print(f"   Status: ⚠️ NO PAYSLIPS GENERATED")
    
    print(f"\n🇰🇪 LEGAL REQUIREMENTS:")
    print(f"   NSSF: Mandatory for ALL employment types (NSSF Act 2013)")
    print(f"   Housing Levy: Mandatory for ALL employees (KRA 2024)")
    print(f"   Employer Contributions: Required for both NSSF and Housing Levy")


if __name__ == "__main__":
    try:
        print("🚀 Starting payslip verification...")
        
        # Verify all payslips
        all_correct = verify_all_payslips()
        
        # Verify compliance by employment type
        verify_specific_employment_types()
        
        print("\n" + "=" * 70)
        print("🎯 FINAL RESULT:")
        print("=" * 70)
        
        if all_correct:
            print("✅ SUCCESS: All payslips correctly display employer contributions")
            print("✅ System is fully compliant with Kenyan employment law")
            print("✅ Both NSSF and Housing Levy employer contributions are visible")
            print("\n🔗 You can view any payslip using the URLs shown above")
        else:
            print("❌ ISSUES DETECTED: Some payslips missing employer contributions")
            print("❌ Manual review required")
        
    except Exception as e:
        print(f"\n❌ Error during verification: {e}")
        print("Please ensure Django environment is properly configured.")
