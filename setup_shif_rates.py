#!/usr/bin/env python
"""
Setup SHIF rates for the payroll system
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

def main():
    print("🔧 Setting up SHIF rates...")
    
    # Check if SHIF rates already exist
    existing_rates = SHIFRate.objects.filter(is_active=True)
    
    if existing_rates.exists():
        print(f"✅ Found {existing_rates.count()} existing SHIF rates:")
        for rate in existing_rates:
            print(f"   - {rate.contribution_rate}% (Min: KES {rate.minimum_contribution}) - {rate.effective_date}")
    else:
        print("❌ No SHIF rates found. Creating default rate...")
        
        # Create SHIF rate: 2.75% with KES 300 minimum
        shif_rate = SHIFRate.objects.create(
            contribution_rate=Decimal('2.75'),
            minimum_contribution=Decimal('300'),
            effective_date=date.today(),
            is_active=True
        )
        
        print(f"✅ Created SHIF rate: {shif_rate.contribution_rate}% (Min: KES {shif_rate.minimum_contribution})")
    
    print("🎉 SHIF rates setup completed!")

if __name__ == '__main__':
    main()
