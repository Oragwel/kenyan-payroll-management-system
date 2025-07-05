from django.db import models
from decimal import Decimal


class PAYETaxBand(models.Model):
    """PAYE tax bands as per KRA regulations"""
    lower_limit = models.DecimalField(max_digits=12, decimal_places=2)
    upper_limit = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2)  # Percentage
    effective_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        if self.upper_limit:
            return f"KES {self.lower_limit:,.0f} - {self.upper_limit:,.0f} @ {self.tax_rate}%"
        return f"KES {self.lower_limit:,.0f} and above @ {self.tax_rate}%"

    class Meta:
        ordering = ['lower_limit']


class NSSFRate(models.Model):
    """NSSF contribution rates"""
    tier = models.IntegerField(choices=[(1, 'Tier 1'), (2, 'Tier 2')])
    lower_limit = models.DecimalField(max_digits=12, decimal_places=2)
    upper_limit = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    contribution_rate = models.DecimalField(max_digits=5, decimal_places=2)  # Percentage
    effective_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"NSSF Tier {self.tier}: KES {self.lower_limit:,.0f} - {self.upper_limit:,.0f} @ {self.contribution_rate}%"

    class Meta:
        ordering = ['tier', 'lower_limit']


class SHIFRate(models.Model):
    """
    Social Health Insurance Fund (SHIF) rates - replaced NHIF in 2024

    SHIF is the new universal health insurance scheme that replaced NHIF
    as part of Kenya's healthcare reforms under the Universal Health Coverage (UHC) initiative.
    """
    contribution_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('2.75'))  # 2.75%
    minimum_contribution = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('300'))
    effective_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"SHIF: {self.contribution_rate}% (Min: KES {self.minimum_contribution})"

    class Meta:
        ordering = ['-effective_date']


class AffordableHousingLevyRate(models.Model):
    """Affordable Housing Levy rates"""
    employee_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('1.5'))  # 1.5%
    employer_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('1.5'))  # 1.5%
    effective_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Housing Levy: Employee {self.employee_rate}%, Employer {self.employer_rate}%"

    class Meta:
        ordering = ['-effective_date']


class TaxRelief(models.Model):
    """Tax reliefs available to employees"""
    RELIEF_TYPE_CHOICES = [
        ('PERSONAL', 'Personal Relief'),
        ('INSURANCE', 'Insurance Relief'),
        ('MORTGAGE', 'Mortgage Interest Relief'),
        ('PENSION', 'Pension Contribution Relief'),
        ('MEDICAL_FUND', 'Post-Retirement Medical Fund Relief'),
    ]

    relief_type = models.CharField(max_length=20, choices=RELIEF_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Percentage
    maximum_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    effective_date = models.DateField()
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_relief_type_display()}"

    class Meta:
        ordering = ['relief_type', '-effective_date']
