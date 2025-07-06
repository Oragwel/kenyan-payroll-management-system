#!/usr/bin/env python3
"""
Test script for all statutory deductions calculations
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append('/home/oragwelr/Desktop/payroll')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payroll.settings')
django.setup()

from statutory_deductions.utils import (
    PAYECalculator, NSSFCalculator,
    SHIFCalculator, AffordableHousingLevyCalculator
)
from decimal import Decimal


def test_all_deductions():
    """Test all statutory deductions with various salary levels"""
    
    print("=== KENYAN STATUTORY DEDUCTIONS TEST ===\n")
    
    # Initialize calculators
    paye_calc = PAYECalculator()
    nssf_calc = NSSFCalculator()
    shif_calc = SHIFCalculator()
    housing_calc = AffordableHousingLevyCalculator()
    
    # Test salaries
    test_salaries = [25000, 50000, 80000, 120000, 200000]
    
    for salary in test_salaries:
        print(f"=== SALARY: KES {salary:,} ===")
        
        # NSSF Calculation
        nssf_result = nssf_calc.calculate_nssf_contribution(salary)
        print(f"NSSF:")
        print(f"  Employee: KES {nssf_result['employee_contribution']:,}")
        print(f"  Employer: KES {nssf_result['employer_contribution']:,}")
        print(f"  Total: KES {nssf_result['total_contribution']:,}")
        
        # SHIF Calculation
        shif_result = shif_calc.calculate_shif_contribution(salary)
        print(f"SHIF:")
        print(f"  Contribution: KES {shif_result['shif_contribution']:,}")
        print(f"  Rate: {shif_result['contribution_rate']}%")
        
        # Housing Levy Calculation
        housing_result = housing_calc.calculate_housing_levy(salary)
        print(f"Housing Levy:")
        print(f"  Employee: KES {housing_result['employee_contribution']:,}")
        print(f"  Employer: KES {housing_result['employer_contribution']:,}")
        print(f"  Total: KES {housing_result['total_contribution']:,}")
        
        # PAYE Calculation (after NSSF deduction)
        taxable_income = salary - nssf_result['employee_contribution']
        paye_result = paye_calc.calculate_paye(taxable_income)
        print(f"PAYE:")
        print(f"  Taxable Income: KES {taxable_income:,}")
        print(f"  Tax: KES {paye_result['paye_tax']:,}")
        print(f"  Effective Rate: {paye_result['effective_tax_rate']:.2f}%")
        
        # Calculate net pay
        total_employee_deductions = (
            nssf_result['employee_contribution'] +
            shif_result['shif_contribution'] +
            housing_result['employee_contribution'] +
            paye_result['paye_tax']
        )
        
        net_pay = salary - total_employee_deductions
        
        print(f"\nSUMMARY:")
        print(f"  Gross Pay: KES {salary:,}")
        print(f"  Total Deductions: KES {total_employee_deductions:,}")
        print(f"  Net Pay: KES {net_pay:,}")
        print(f"  Take-home %: {(net_pay/salary*100):.1f}%")
        
        print("-" * 60)
    
    # Test NSSF tiers specifically
    print("\n=== NSSF TIER TESTING ===\n")
    
    test_nssf_salaries = [5000, 7000, 10000, 20000, 36000, 50000]
    
    for salary in test_nssf_salaries:
        nssf_result = nssf_calc.calculate_nssf_contribution(salary)
        print(f"Salary: KES {salary:,}")
        print(f"  Tier 1: KES {nssf_result['tier_1_contribution']:,}")
        print(f"  Tier 2: KES {nssf_result['tier_2_contribution']:,}")
        print(f"  Employee Total: KES {nssf_result['employee_contribution']:,}")
        
        # Show breakdown
        for breakdown in nssf_result['contribution_breakdown']:
            print(f"    Tier {breakdown['tier']}: KES {breakdown['pensionable_amount']:,} @ {breakdown['rate']}% = KES {breakdown['employee_contribution']:,}")
        print()


def test_edge_cases():
    """Test edge cases and boundary conditions"""
    print("=== EDGE CASES TEST ===\n")
    
    calculators = {
        'NSSF': NSSFCalculator(),
        'SHIF': SHIFCalculator(),
        'Housing': AffordableHousingLevyCalculator(),
        'PAYE': PAYECalculator()
    }
    
    # Test zero salary
    print("Testing zero salary:")
    for name, calc in calculators.items():
        if name == 'NSSF':
            result = calc.calculate_nssf_contribution(0)
            print(f"  {name}: KES {result['employee_contribution']:,}")
        elif name == 'SHIF':
            result = calc.calculate_shif_contribution(0)
            print(f"  {name}: KES {result['shif_contribution']:,}")
        elif name == 'Housing':
            result = calc.calculate_housing_levy(0)
            print(f"  {name}: KES {result['employee_contribution']:,}")
        elif name == 'PAYE':
            result = calc.calculate_paye(0)
            print(f"  {name}: KES {result['paye_tax']:,}")
    
    print("\nTesting boundary values:")
    
    # Test NSSF boundaries
    nssf_calc = calculators['NSSF']
    boundary_salaries = [6999, 7000, 7001, 35999, 36000, 36001]
    
    for salary in boundary_salaries:
        result = nssf_calc.calculate_nssf_contribution(salary)
        print(f"  NSSF @ KES {salary:,}: Employee KES {result['employee_contribution']:,}")


if __name__ == '__main__':
    test_all_deductions()
    test_edge_cases()
