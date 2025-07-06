#!/usr/bin/env python3
"""
Test script for PAYE calculation
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append('/home/oragwelr/Desktop/payroll')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payroll.settings')
django.setup()

from statutory_deductions.utils import PAYECalculator
from decimal import Decimal


def test_paye_calculations():
    """Test PAYE calculations with various scenarios"""
    calculator = PAYECalculator()
    
    print("=== PAYE Tax Calculator Test ===\n")
    
    # Test scenarios
    test_cases = [
        {
            'name': 'Low income (KES 20,000)',
            'income': 20000,
            'expected_tax_range': (0, 2000)  # Should be around 10% after relief
        },
        {
            'name': 'Middle income (KES 50,000)',
            'income': 50000,
            'expected_tax_range': (5000, 8000)
        },
        {
            'name': 'High income (KES 100,000)',
            'income': 100000,
            'expected_tax_range': (18000, 22000)
        },
        {
            'name': 'Very high income (KES 200,000)',
            'income': 200000,
            'expected_tax_range': (45000, 55000)
        }
    ]
    
    for test_case in test_cases:
        print(f"Testing: {test_case['name']}")
        print(f"Gross Income: KES {test_case['income']:,}")
        
        result = calculator.calculate_paye(test_case['income'])
        
        print(f"Taxable Income: KES {result['taxable_income']:,}")
        print(f"Income after deductions: KES {result['income_after_deductions']:,}")
        print(f"Tax before relief: KES {result['tax_before_relief']:,}")
        print(f"Personal relief: KES {result['tax_reliefs']['personal_relief']:,}")
        print(f"PAYE Tax: KES {result['paye_tax']:,}")
        print(f"Effective tax rate: {result['effective_tax_rate']:.2f}%")
        
        # Check if result is within expected range
        min_expected, max_expected = test_case['expected_tax_range']
        if min_expected <= result['paye_tax'] <= max_expected:
            print("✓ PASS - Tax amount within expected range")
        else:
            print(f"✗ FAIL - Expected {min_expected}-{max_expected}, got {result['paye_tax']}")
        
        print("-" * 50)
    
    # Test with deductions and reliefs
    print("\n=== Testing with Deductions and Reliefs ===\n")
    
    income = 80000
    insurance_premiums = 5000
    mortgage_interest = 25000
    pension_contribution = 10000
    
    result = calculator.calculate_paye(
        taxable_income=income,
        insurance_premiums=insurance_premiums,
        mortgage_interest=mortgage_interest,
        pension_contribution=pension_contribution
    )
    
    print(f"Gross Income: KES {income:,}")
    print(f"Insurance Premiums: KES {insurance_premiums:,}")
    print(f"Mortgage Interest: KES {mortgage_interest:,}")
    print(f"Pension Contribution: KES {pension_contribution:,}")
    print()
    print("Calculation Results:")
    print(f"Allowable Deductions: KES {result['allowable_deductions']['total']:,}")
    print(f"  - Mortgage Interest: KES {result['allowable_deductions']['mortgage_interest']:,}")
    print(f"  - Pension Contribution: KES {result['allowable_deductions']['pension_contribution']:,}")
    print(f"Income after deductions: KES {result['income_after_deductions']:,}")
    print(f"Tax before relief: KES {result['tax_before_relief']:,}")
    print(f"Tax Reliefs: KES {result['tax_reliefs']['total']:,}")
    print(f"  - Personal Relief: KES {result['tax_reliefs']['personal_relief']:,}")
    print(f"  - Insurance Relief: KES {result['tax_reliefs']['insurance_relief']:,}")
    print(f"Final PAYE Tax: KES {result['paye_tax']:,}")
    print(f"Effective tax rate: {result['effective_tax_rate']:.2f}%")
    
    # Display tax bands
    print("\n=== Current Tax Bands ===\n")
    bands = calculator.get_tax_bands_info()
    for band in bands:
        if band['upper_limit']:
            print(f"KES {band['lower_limit']:,} - {band['upper_limit']:,}: {band['tax_rate']}%")
        else:
            print(f"KES {band['lower_limit']:,} and above: {band['tax_rate']}%")


if __name__ == '__main__':
    test_paye_calculations()
