from django.db import models
from django.core.validators import RegexValidator


class Company(models.Model):
    """Company information model for payroll system"""
    
    name = models.CharField(max_length=200, help_text="Official company name")
    trading_name = models.CharField(max_length=200, blank=True, help_text="Trading or business name (if different)")
    
    # Contact Information
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=50, default="Kenya")
    
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)
    
    # Kenyan Business Registration
    kra_pin_validator = RegexValidator(
        regex=r'^P\d{9}[A-Z]$',
        message='Company KRA PIN must be in format: P123456789A'
    )
    kra_pin = models.CharField(
        max_length=11,
        validators=[kra_pin_validator],
        unique=True,
        help_text='Company KRA PIN in format: P123456789A'
    )
    
    business_registration_number = models.CharField(
        max_length=20,
        unique=True,
        help_text="Business registration number from Registrar of Companies"
    )
    
    nssf_employer_number = models.CharField(
        max_length=20,
        blank=True,
        help_text="NSSF employer registration number"
    )
    
    shif_employer_number = models.CharField(
        max_length=20,
        blank=True,
        help_text="SHIF employer registration number"
    )
    
    # Logo and Branding
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    
    # Payroll Settings
    default_pay_day = models.IntegerField(
        default=25,
        help_text="Default day of month for salary payments (1-31)"
    )
    
    # Status
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @property
    def full_address(self):
        """Get formatted full address"""
        address_parts = [self.address_line_1]
        if self.address_line_2:
            address_parts.append(self.address_line_2)
        address_parts.append(self.city)
        if self.postal_code:
            address_parts.append(self.postal_code)
        address_parts.append(self.country)
        return ", ".join(address_parts)
    
    @property
    def display_name(self):
        """Get display name (trading name if available, otherwise official name)"""
        return self.trading_name if self.trading_name else self.name
    
    class Meta:
        verbose_name_plural = "Companies"
        ordering = ['name']


class CompanySettings(models.Model):
    """Company-specific payroll settings"""
    
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='settings')
    
    # Payroll Configuration
    payroll_frequency = models.CharField(
        max_length=10,
        choices=[
            ('MONTHLY', 'Monthly'),
            ('WEEKLY', 'Weekly'),
            ('BIWEEKLY', 'Bi-weekly'),
        ],
        default='MONTHLY'
    )
    
    # Tax and Statutory Settings
    enable_paye = models.BooleanField(default=True, help_text="Enable PAYE tax calculations")
    enable_nssf = models.BooleanField(default=True, help_text="Enable NSSF contributions")
    enable_shif = models.BooleanField(default=True, help_text="Enable SHIF contributions")
    enable_housing_levy = models.BooleanField(default=True, help_text="Enable Housing Levy")
    
    # Payslip Settings
    include_employer_contributions = models.BooleanField(
        default=True,
        help_text="Show employer contributions on payslips"
    )
    
    payslip_footer_text = models.TextField(
        blank=True,
        help_text="Custom footer text for payslips"
    )
    
    # Approval Settings
    require_payroll_approval = models.BooleanField(
        default=True,
        help_text="Require approval before payroll processing"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Settings for {self.company.name}"
    
    class Meta:
        verbose_name_plural = "Company Settings"
