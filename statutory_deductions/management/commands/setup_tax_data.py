"""
Management command to set up initial tax data for Kenya
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from statutory_deductions.models import (
    PAYETaxBand, TaxRelief, NSSFRate,
    SHIFRate, AffordableHousingLevyRate
)


class Command(BaseCommand):
    help = 'Set up initial Kenyan tax data (PAYE bands, reliefs, NSSF, SHIF rates)'

    def handle(self, *args, **options):
        self.stdout.write('Setting up Kenyan tax data...')
        
        # Set up PAYE tax bands (as per Finance Act 2023)
        self.setup_paye_bands()
        
        # Set up tax reliefs
        self.setup_tax_reliefs()
        
        # Set up NSSF rates
        self.setup_nssf_rates()

        # Set up SHIF rates
        self.setup_shif_rates()
        
        # Set up Affordable Housing Levy
        self.setup_housing_levy()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully set up Kenyan tax data!')
        )

    def setup_paye_bands(self):
        """Set up PAYE tax bands as per Finance Act 2023"""
        self.stdout.write('Setting up PAYE tax bands...')

        # Check if PAYE bands already exist
        existing_bands = PAYETaxBand.objects.filter(is_active=True)
        if existing_bands.exists():
            self.stdout.write('✓ PAYE tax bands already exist - preserving existing data')
            return
        
        # Current PAYE bands (effective July 1, 2023)
        bands = [
            {'lower': 0, 'upper': 24000, 'rate': 10},
            {'lower': 24001, 'upper': 32333, 'rate': 25},
            {'lower': 32334, 'upper': 500000, 'rate': 30},
            {'lower': 500001, 'upper': 800000, 'rate': 32.5},
            {'lower': 800001, 'upper': None, 'rate': 35},  # No upper limit
        ]
        
        for band_data in bands:
            PAYETaxBand.objects.create(
                lower_limit=Decimal(str(band_data['lower'])),
                upper_limit=Decimal(str(band_data['upper'])) if band_data['upper'] else None,
                tax_rate=Decimal(str(band_data['rate'])),
                effective_date=timezone.now().date(),
                is_active=True
            )
        
        self.stdout.write('✓ PAYE tax bands set up')

    def setup_tax_reliefs(self):
        """Set up tax reliefs"""
        self.stdout.write('Setting up tax reliefs...')

        # Check if tax reliefs already exist
        existing_reliefs = TaxRelief.objects.filter(is_active=True)
        if existing_reliefs.exists():
            self.stdout.write('✓ Tax reliefs already exist - preserving existing data')
            return
        
        # Personal relief
        TaxRelief.objects.create(
            relief_type='PERSONAL',
            amount=Decimal('2400'),  # KES 2,400 per month
            effective_date=timezone.now().date(),
            is_active=True,
            description='Personal relief for all resident individuals'
        )
        
        # Insurance relief
        TaxRelief.objects.create(
            relief_type='INSURANCE',
            rate=Decimal('15'),  # 15% of premiums
            maximum_amount=Decimal('5000'),  # KES 60,000 per year / 12 months
            effective_date=timezone.now().date(),
            is_active=True,
            description='Insurance relief at 15% of premiums, max KES 60,000 per year'
        )
        
        # Mortgage interest relief
        TaxRelief.objects.create(
            relief_type='MORTGAGE',
            maximum_amount=Decimal('30000'),  # KES 30,000 per month
            effective_date=timezone.now().date(),
            is_active=True,
            description='Mortgage interest relief, max KES 30,000 per month'
        )
        
        # Pension contribution relief
        TaxRelief.objects.create(
            relief_type='PENSION',
            maximum_amount=Decimal('30000'),  # KES 30,000 per month
            effective_date=timezone.now().date(),
            is_active=True,
            description='Pension contribution relief, max KES 30,000 per month'
        )
        
        # Post-retirement medical fund relief
        TaxRelief.objects.create(
            relief_type='MEDICAL_FUND',
            maximum_amount=Decimal('15000'),  # KES 15,000 per month
            effective_date=timezone.now().date(),
            is_active=True,
            description='Post-retirement medical fund relief, max KES 15,000 per month'
        )
        
        self.stdout.write('✓ Tax reliefs set up')

    def setup_nssf_rates(self):
        """Set up NSSF rates (effective February 2024)"""
        self.stdout.write('Setting up NSSF rates...')

        # Check if NSSF rates already exist
        existing_rates = NSSFRate.objects.filter(is_active=True)
        if existing_rates.exists():
            self.stdout.write('✓ NSSF rates already exist - preserving existing data')
            return
        
        # Tier 1: KES 7,000 limit, 6% contribution
        NSSFRate.objects.create(
            tier=1,
            lower_limit=Decimal('0'),
            upper_limit=Decimal('7000'),
            contribution_rate=Decimal('6'),
            effective_date=timezone.now().date(),
            is_active=True
        )
        
        # Tier 2: KES 36,000 limit, 6% on excess above KES 7,000
        NSSFRate.objects.create(
            tier=2,
            lower_limit=Decimal('7001'),
            upper_limit=Decimal('36000'),
            contribution_rate=Decimal('6'),
            effective_date=timezone.now().date(),
            is_active=True
        )
        
        self.stdout.write('✓ NSSF rates set up')

    def setup_shif_rates(self):
        """Set up SHIF rates (Social Health Insurance Fund - replaced NHIF in 2024)"""
        self.stdout.write('Setting up SHIF rates...')
        self.stdout.write('Note: SHIF replaced NHIF as part of Universal Health Coverage reforms')

        # Check if SHIF rates already exist
        existing_rates = SHIFRate.objects.filter(is_active=True)
        if existing_rates.exists():
            self.stdout.write('✓ SHIF rates already exist - preserving existing data')
            return

        # SHIF: 2.75% of gross salary, minimum KES 300
        SHIFRate.objects.create(
            contribution_rate=Decimal('2.75'),
            minimum_contribution=Decimal('300'),
            effective_date=timezone.now().date(),
            is_active=True
        )

        self.stdout.write('✓ SHIF rates set up (replaced NHIF)')

    def setup_housing_levy(self):
        """Set up Affordable Housing Levy rates"""
        self.stdout.write('Setting up Affordable Housing Levy rates...')

        # Check if housing levy rates already exist
        existing_rates = AffordableHousingLevyRate.objects.filter(is_active=True)
        if existing_rates.exists():
            self.stdout.write('✓ Housing levy rates already exist - preserving existing data')
            return
        
        # Housing Levy: 1.5% each for employee and employer
        AffordableHousingLevyRate.objects.create(
            employee_rate=Decimal('1.5'),
            employer_rate=Decimal('1.5'),
            effective_date=timezone.now().date(),
            is_active=True
        )
        
        self.stdout.write('✓ Affordable Housing Levy rates set up')
