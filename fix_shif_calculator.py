#!/usr/bin/env python
"""
Fix SHIF calculator by ensuring proper SHIF rates are set up
"""

import os
import sys
import django
from decimal import Decimal
from datetime import date

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payroll.settings.production')
django.setup()

from statutory_deductions.models import SHIFRate
from statutory_deductions.utils import SHIFCalculator

def setup_shif_rates():
    """Set up SHIF rates if they don't exist"""
    print("🔍 Checking SHIF rates...")
    
    # Check existing rates
    existing_rates = SHIFRate.objects.filter(is_active=True)
    print(f"Found {existing_rates.count()} active SHIF rates")
    
    for rate in existing_rates:
        print(f"  - Rate: {rate.contribution_rate}%, Min: KES {rate.minimum_contribution}, Date: {rate.effective_date}")
    
    if not existing_rates.exists():
        print("❌ No active SHIF rates found. Creating default rate...")
        
        # Create default SHIF rate
        shif_rate = SHIFRate.objects.create(
            contribution_rate=Decimal('2.75'),  # 2.75%
            minimum_contribution=Decimal('300'),  # KES 300 minimum
            effective_date=date.today(),
            is_active=True
        )
        print(f"✅ Created SHIF rate: {shif_rate}")
    else:
        print("✅ SHIF rates already exist")

def test_shif_calculation():
    """Test SHIF calculation with various salaries"""
    print("\n🧮 Testing SHIF calculations...")
    
    calc = SHIFCalculator()
    test_salaries = [10000, 25000, 50000, 100000, 200000]
    
    for salary in test_salaries:
        result = calc.calculate_shif_contribution(Decimal(str(salary)))
        print(f"  Salary: KES {salary:,} → SHIF: KES {result['shif_contribution']:,}")

def main():
    print("🔧 Fixing SHIF Calculator...")
    setup_shif_rates()
    test_shif_calculation()
    print("\n✅ SHIF calculator fix completed!")

if __name__ == '__main__':
    main()
