from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Organization(models.Model):
    """Organization/Entity model for payroll system - supports Companies, Government, NGOs, etc."""

    ORGANIZATION_TYPES = [
        ('COMPANY', 'Private Company'),
        ('GOVERNMENT', 'Government Entity'),
        ('PARASTATAL', 'Parastatal/State Corporation'),
        ('NGO', 'Non-Governmental Organization'),
        ('INTERNATIONAL', 'International Organization'),
        ('COOPERATIVE', 'Cooperative Society'),
        ('INSTITUTION', 'Educational/Training Institution'),
        ('RELIGIOUS', 'Religious Organization'),
        ('OTHER', 'Other Organization'),
    ]

    # Basic Information
    organization_type = models.CharField(
        max_length=20,
        choices=ORGANIZATION_TYPES,
        default='COMPANY',
        help_text="Type of organization"
    )

    name = models.CharField(max_length=200, help_text="Official organization name")
    short_name = models.CharField(max_length=100, blank=True, help_text="Short name or acronym (e.g., KRA, NHIF)")
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

    # Government/Organization Specific Fields
    ministry = models.CharField(
        max_length=200,
        blank=True,
        help_text="Parent ministry (for government entities)"
    )

    sector = models.CharField(
        max_length=100,
        blank=True,
        help_text="Sector/Industry (e.g., Health, Education, Finance)"
    )

    # Registration and Compliance
    kra_pin_validator = RegexValidator(
        regex=r'^P\d{9}[A-Z]$',
        message='Organization KRA PIN must be in format: P123456789A'
    )
    kra_pin = models.CharField(
        max_length=11,
        validators=[kra_pin_validator],
        unique=True,
        help_text='Organization KRA PIN in format: P123456789A'
    )

    registration_number = models.CharField(
        max_length=50,
        blank=True,
        help_text="Registration number (Business/Government/NGO registration)"
    )

    registration_authority = models.CharField(
        max_length=100,
        blank=True,
        help_text="Registration authority (e.g., Registrar of Companies, NGO Board)"
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

    # Logo and Branding - temporarily disabled due to Python 3.13 Pillow compatibility
    # logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    logo = models.CharField(max_length=255, blank=True, null=True, help_text="Logo path - temporarily disabled for Python 3.13 compatibility")

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
        """Get display name based on organization type"""
        if self.short_name:
            return f"{self.name} ({self.short_name})"
        elif self.trading_name:
            return self.trading_name
        else:
            return self.name

    @property
    def organization_hierarchy(self):
        """Get full organizational hierarchy"""
        hierarchy = []
        if self.ministry:
            hierarchy.append(self.ministry)
        hierarchy.append(self.name)
        return " → ".join(hierarchy)

    @property
    def is_government_entity(self):
        """Check if this is a government entity"""
        return self.organization_type in ['GOVERNMENT', 'PARASTATAL']

    @property
    def registration_display(self):
        """Get formatted registration information"""
        if self.registration_number and self.registration_authority:
            return f"{self.registration_number} ({self.registration_authority})"
        elif self.registration_number:
            return self.registration_number
        else:
            return "Not specified"

    class Meta:
        verbose_name_plural = "Organizations"
        ordering = ['organization_type', 'name']


class Department(models.Model):
    """Department model for organizing employees within organizations"""
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        ordering = ['organization__name', 'name']
        unique_together = [['organization', 'name'], ['organization', 'code']]


class JobTitle(models.Model):
    """Job titles for employees"""
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Employee(models.Model):
    """Employee model with Kenyan employment structure"""

    EMPLOYMENT_TYPE_CHOICES = [
        ('PERMANENT', 'Permanent Employee'),
        ('CONTRACT', 'Contract Employee'),
        ('CASUAL', 'Casual Worker'),
        ('INTERN', 'Intern'),
    ]

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('SINGLE', 'Single'),
        ('MARRIED', 'Married'),
        ('DIVORCED', 'Divorced'),
        ('WIDOWED', 'Widowed'),
    ]

    # Personal Information
    payroll_number = models.CharField(max_length=20, unique=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, blank=True, null=True)

    # Contact Information
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    # National Identification
    national_id = models.CharField(
        max_length=8,
        unique=True,
        blank=True,
        null=True,
        help_text='Kenyan National ID number (8 digits)'
    )

    # Employment Information
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    job_title = models.ForeignKey(JobTitle, on_delete=models.PROTECT)
    employment_type = models.CharField(max_length=10, choices=EMPLOYMENT_TYPE_CHOICES)
    date_hired = models.DateField(blank=True, null=True)
    date_terminated = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    # Kenyan Statutory Information
    kra_pin_validator = RegexValidator(
        regex=r'^[A-Z]\d{9}[A-Z]$',
        message='KRA PIN must be in format: A123456789B'
    )
    kra_pin = models.CharField(
        max_length=11,
        validators=[kra_pin_validator],
        unique=True,
        blank=True,
        null=True,
        help_text='KRA PIN in format: A123456789B (Optional)'
    )

    nssf_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    shif_number = models.CharField(max_length=20, blank=True, null=True, unique=True, help_text="SHIF membership number (Social Health Insurance Fund)")

    # Bank Information
    BANK_CHOICES = [
        ('12053', '12053'),
        ('68058', '68058'),
        ('01169', '01169'),
        ('11081', '11081'),
        ('03017', '03017'),
        ('74004', '74004'),
        ('72006', '72006'),
    ]

    bank_code = models.CharField(max_length=10, choices=BANK_CHOICES, blank=True, null=True)
    bank_name = models.CharField(max_length=100)
    bank_branch = models.CharField(max_length=100, blank=True, null=True)
    account_number = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_bank_name_from_code(self):
        """Get bank name from bank code"""
        # Create a mapping of code to just the bank name (without the code prefix)
        bank_name_mapping = {
            '12053': 'National Bank',
            '68058': 'Equity Bank',
            '01169': 'KCB Bank',
            '11081': 'Cooperative Bank',
            '03017': 'Absa Bank',
            '74004': 'Premier Bank',
            '72006': 'Gulf African Bank',
        }
        return bank_name_mapping.get(self.bank_code, '')

    def get_full_bank_info(self):
        """Get formatted bank information with code and name"""
        if self.bank_code and self.bank_name:
            return f"{self.bank_name} ({self.bank_code})"
        elif self.bank_name:
            return self.bank_name
        elif self.bank_code:
            return f"Code: {self.bank_code}"
        return "Not specified"

    def save(self, *args, **kwargs):
        if not self.payroll_number:
            self.payroll_number = self.generate_payroll_number()

        # Handle empty fields - convert empty strings to None for optional fields that allow NULL
        if self.national_id == '':
            self.national_id = None
        if self.email == '':
            self.email = None

        # For fields that don't allow NULL in current schema, keep placeholder values
        # These will be handled by the form validation

        # Handle other optional fields
        if self.middle_name == '':
            self.middle_name = ''  # Keep as empty string for now
        if self.address == '':
            self.address = ''  # Keep as empty string for now
        if self.bank_branch == '':
            self.bank_branch = ''  # Keep as empty string for now
        if self.bank_code == '':
            self.bank_code = ''  # Keep as empty string for now
        if self.gender == '':
            self.gender = ''  # Keep as empty string for now
        if self.marital_status == '':
            self.marital_status = ''  # Keep as empty string for now

        # Auto-populate bank name from bank code if bank code is selected
        # Only auto-populate if bank name is empty or if it matches a bank code value
        if self.bank_code:
            bank_name_from_code = self.get_bank_name_from_code()
            if not self.bank_name or self.bank_name == bank_name_from_code:
                self.bank_name = bank_name_from_code

        super().save(*args, **kwargs)

    def generate_payroll_number(self):
        """Generate auto-incremented payroll number"""
        last_employee = Employee.objects.order_by('id').last()
        if last_employee:
            # Extract number from last payroll number and increment
            try:
                last_number = int(last_employee.payroll_number.replace('PAY', ''))
                new_number = last_number + 1
            except (ValueError, AttributeError):
                # Fallback if existing numbers don't follow pattern
                new_number = Employee.objects.count() + 1
        else:
            new_number = 1

        return f"PAY{new_number:04d}"  # Format: PAY0001, PAY0002, etc.

    def __str__(self):
        return f"{self.payroll_number} - {self.first_name} {self.last_name}"

    @property
    def full_name(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['payroll_number']


class SalaryStructure(models.Model):
    """Salary structure for employees"""
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='salary_structure')

    # Basic Salary Components
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2)

    # Allowances
    house_allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    transport_allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    medical_allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    lunch_allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    communication_allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other_allowances = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Benefits (non-cash)
    car_benefit_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    housing_benefit_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Insurance and Pension
    life_insurance_premium = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    health_insurance_premium = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    education_insurance_premium = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Mortgage Interest (for tax relief)
    mortgage_interest = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Post-retirement medical fund
    post_retirement_medical_fund = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Pension contributions
    pension_contribution = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    effective_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Salary Structure for {self.employee.full_name}"

    @property
    def gross_salary(self):
        """Calculate gross salary including all allowances and benefits"""
        return (
            (self.basic_salary or 0) +
            (self.house_allowance or 0) +
            (self.transport_allowance or 0) +
            (self.medical_allowance or 0) +
            (self.lunch_allowance or 0) +
            (self.communication_allowance or 0) +
            (self.other_allowances or 0) +
            (self.car_benefit_value or 0) +
            (self.housing_benefit_value or 0)
        )

    @property
    def total_allowances(self):
        """Calculate total cash allowances"""
        return (
            (self.house_allowance or 0) +
            (self.transport_allowance or 0) +
            (self.medical_allowance or 0) +
            (self.lunch_allowance or 0) +
            (self.communication_allowance or 0) +
            (self.other_allowances or 0)
        )

    @property
    def total_benefits(self):
        """Calculate total non-cash benefits"""
        return (self.car_benefit_value or 0) + (self.housing_benefit_value or 0)

    class Meta:
        ordering = ['-effective_date']
