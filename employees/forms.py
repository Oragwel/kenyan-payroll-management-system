"""
Forms for employee management
"""
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Employee, Department, JobTitle, SalaryStructure, Organization
import re
# import pandas as pd  # Temporarily disabled for deployment
from io import BytesIO


class EmployeeForm(forms.ModelForm):
    """Form for creating and updating employees"""

    # Override fields to remove model validators for optional handling
    kra_pin = forms.CharField(
        max_length=11,
        required=False,
        help_text='KRA PIN in format: A123456789B (Optional - leave empty if not available)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Optional - leave empty if not available'
        })
    )

    nssf_number = forms.CharField(
        max_length=20,
        required=False,
        help_text='NSSF number (Optional)',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional'})
    )

    shif_number = forms.CharField(
        max_length=20,
        required=False,
        help_text='SHIF membership number (Optional)',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional'})
    )

    class Meta:
        model = Employee
        fields = [
            'first_name', 'middle_name', 'last_name',
            'date_of_birth', 'gender', 'marital_status', 'national_id', 'email', 'phone_number',
            'address', 'department', 'job_title', 'employment_type', 'date_hired',
            'kra_pin', 'nssf_number', 'shif_number', 'bank_code', 'bank_name', 'bank_branch',
            'account_number'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Optional'}),
            'date_hired': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Optional'}),
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional - Employee address'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Optional - employee@company.com'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'national_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional - 12345678'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'marital_status': forms.Select(attrs={'class': 'form-control'}),
            # kra_pin, nssf_number, shif_number are overridden as form fields above
            'bank_code': forms.Select(attrs={'class': 'form-control'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_branch': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional - e.g., Nairobi Branch'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'job_title': forms.Select(attrs={'class': 'form-control'}),
            'employment_type': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get the active organization
        from .models import Organization
        try:
            active_org = Organization.objects.filter(is_active=True).first()
            if active_org:
                # Filter departments by active organization
                self.fields['department'].queryset = Department.objects.filter(organization=active_org)
            else:
                # If no active organization, show all departments
                self.fields['department'].queryset = Department.objects.all()
        except:
            # Fallback to all departments if there's an error
            self.fields['department'].queryset = Department.objects.all()

        # Configure department dropdown
        self.fields['department'].widget.attrs.update({'class': 'form-control'})
        self.fields['department'].empty_label = "--- Select Department ---"

        # Configure job title dropdown
        self.fields['job_title'].widget.attrs.update({'class': 'form-control'})
        self.fields['job_title'].empty_label = "--- Select Job Title ---"
        self.fields['job_title'].queryset = JobTitle.objects.all()

        # Configure employment type dropdown
        self.fields['employment_type'].widget.attrs.update({'class': 'form-control'})

        # Configure bank code dropdown
        self.fields['bank_code'].widget.attrs.update({'class': 'form-control'})
        self.fields['bank_code'].empty_label = "--- Select Bank Code (Optional) ---"
        self.fields['bank_code'].required = False

        # Set field requirements based on new specifications
        # MANDATORY FIELDS
        self.fields['account_number'].required = True

        # OPTIONAL FIELDS
        self.fields['national_id'].required = False
        self.fields['gender'].required = False
        self.fields['phone_number'].required = False
        self.fields['kra_pin'].required = False
        self.fields['shif_number'].required = False
        self.fields['nssf_number'].required = False
        self.fields['bank_branch'].required = False
        self.fields['middle_name'].required = False
        self.fields['address'].required = False
        self.fields['email'].required = False
        self.fields['bank_code'].required = False

        # Add empty choice for optional fields
        self.fields['gender'].choices = [('', '--- Select Gender (Optional) ---')] + list(self.fields['gender'].choices)
        self.fields['marital_status'].choices = [('', '--- Select Marital Status (Optional) ---')] + list(self.fields['marital_status'].choices)
        self.fields['marital_status'].required = False
        self.fields['date_of_birth'].required = False
        self.fields['address'].required = False
        self.fields['email'].required = False
        self.fields['date_hired'].required = False

    def clean_national_id(self):
        """Validate National ID format and uniqueness - OPTIONAL but UNIQUE if provided"""
        national_id = self.cleaned_data.get('national_id')

        # National ID is now optional
        if not national_id:
            return None

        # Remove any spaces or dashes
        national_id = re.sub(r'[\s-]', '', national_id)

        # Check format: 8 digits
        if not re.match(r'^\d{8}$', national_id):
            raise ValidationError('National ID must be exactly 8 digits')

        # Check if National ID already exists (excluding current instance)
        existing = Employee.objects.filter(national_id=national_id)
        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        if existing.exists():
            raise ValidationError('An employee with this National ID already exists')

        return national_id

    def clean_gender(self):
        """Handle optional gender field - return empty string for database compatibility"""
        gender = self.cleaned_data.get('gender')
        return gender if gender else ''

    def clean_marital_status(self):
        """Handle optional marital status field - return empty string for database compatibility"""
        marital_status = self.cleaned_data.get('marital_status')
        return marital_status if marital_status else ''

    def clean_middle_name(self):
        """Handle optional middle name field - return empty string for database compatibility"""
        middle_name = self.cleaned_data.get('middle_name')
        return middle_name if middle_name else ''

    def clean_address(self):
        """Handle optional address field - return empty string for database compatibility"""
        address = self.cleaned_data.get('address')
        return address if address else ''

    def clean_bank_branch(self):
        """Handle optional bank branch field - return empty string for database compatibility"""
        bank_branch = self.cleaned_data.get('bank_branch')
        return bank_branch if bank_branch else ''

    def clean_bank_code(self):
        """Handle optional bank code field - return empty string for database compatibility"""
        bank_code = self.cleaned_data.get('bank_code')
        return bank_code if bank_code else ''

    def clean_kra_pin(self):
        """KRA PIN validation - only runs for non-empty values due to full_clean preprocessing"""
        kra_pin = self.cleaned_data.get('kra_pin', '')

        # If it's already a placeholder (from full_clean), return as-is
        if kra_pin.startswith('EMPTY_KRA_'):
            return kra_pin

        # If empty somehow, create placeholder
        if not kra_pin or kra_pin.strip() == '':
            import uuid
            return f"EMPTY_KRA_{uuid.uuid4().hex[:8].upper()}"

        # If user provided a real value, validate it
        kra_pin_clean = re.sub(r'[^A-Z0-9]', '', kra_pin.upper())

        # Check format
        if not re.match(r'^A\d{9}[A-Z]$', kra_pin_clean):
            raise ValidationError('KRA PIN must be in format A123456789B (A + 9 digits + letter)')

        # Check uniqueness
        existing = Employee.objects.filter(kra_pin=kra_pin_clean)
        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        if existing.exists():
            raise ValidationError('An employee with this KRA PIN already exists')

        return kra_pin_clean

    def clean_nssf_number(self):
        """Validate NSSF number uniqueness - OPTIONAL but UNIQUE if provided"""
        nssf_number = self.cleaned_data.get('nssf_number')

        # NSSF number is optional - generate unique placeholder if empty
        if not nssf_number:
            import uuid
            return f"EMPTY_NSSF_{uuid.uuid4().hex[:8].upper()}"

        # Check if NSSF number already exists (excluding current instance)
        existing = Employee.objects.filter(nssf_number=nssf_number)
        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        if existing.exists():
            raise ValidationError('An employee with this NSSF number already exists')

        return nssf_number

    def clean_shif_number(self):
        """Validate SHIF number uniqueness - OPTIONAL but UNIQUE if provided"""
        shif_number = self.cleaned_data.get('shif_number')

        # SHIF number is optional - generate unique placeholder if empty
        if not shif_number:
            import uuid
            return f"EMPTY_SHIF_{uuid.uuid4().hex[:8].upper()}"

        # Check if SHIF number already exists (excluding current instance)
        existing = Employee.objects.filter(shif_number=shif_number)
        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        if existing.exists():
            raise ValidationError('An employee with this SHIF number already exists')

        return shif_number

    def clean_email(self):
        """Handle optional email field - generate unique placeholder for empty to avoid UNIQUE constraint issues"""
        email = self.cleaned_data.get('email')
        if not email:
            # Generate unique placeholder for empty email to avoid constraint issues
            import uuid
            return f"empty_email_{uuid.uuid4().hex[:8]}@placeholder.local"
        return email

    def clean(self):
        """Override clean method to ensure all optional fields have proper default values"""
        try:
            cleaned_data = super().clean()
        except ValidationError as e:
            # If there are validation errors, handle them gracefully
            cleaned_data = self.cleaned_data

        # Always clear validation errors for empty optional fields
        if hasattr(self, '_errors'):
            optional_fields = ['kra_pin', 'nssf_number', 'shif_number', 'middle_name', 'address', 'gender', 'marital_status', 'bank_branch', 'bank_code', 'email']
            for field in optional_fields:
                field_value = self.data.get(field, '').strip()
                if field in self._errors and (not field_value or field_value == ''):
                    # Remove validation errors for empty optional fields
                    del self._errors[field]
                    # Ensure the field gets a proper default value
                    if field not in cleaned_data:
                        cleaned_data[field] = ''

        # Ensure all optional fields that might have NOT NULL constraints get default values
        optional_fields_with_defaults = {
            'middle_name': '',
            'address': '',
            'gender': '',
            'marital_status': '',
            'bank_branch': '',
            'bank_code': '',
        }

        # Unique fields that need special handling
        unique_fields_with_placeholders = {
            'kra_pin': 'EMPTY_KRA',
            'nssf_number': 'EMPTY_NSSF',
            'shif_number': 'EMPTY_SHIF',
            'email': 'empty_email',
        }

        # Set defaults for optional fields
        for field, default_value in optional_fields_with_defaults.items():
            if not cleaned_data.get(field):
                cleaned_data[field] = default_value

        # Set unique placeholders for unique fields
        import uuid
        for field, prefix in unique_fields_with_placeholders.items():
            if not cleaned_data.get(field):
                if field == 'email':
                    cleaned_data[field] = f"{prefix}_{uuid.uuid4().hex[:8]}@placeholder.local"
                else:
                    cleaned_data[field] = f"{prefix}_{uuid.uuid4().hex[:8].upper()}"

        return cleaned_data

    def full_clean(self):
        """Override full_clean to completely bypass validation for empty optional fields"""
        # Pre-process the data to handle empty optional fields
        if hasattr(self, 'data') and self.data:
            # Create a mutable copy of the data
            data = self.data.copy()

            # For KRA PIN specifically - if empty, set a placeholder immediately
            if 'kra_pin' in data and (not data['kra_pin'] or data['kra_pin'].strip() == ''):
                import uuid
                data['kra_pin'] = f"EMPTY_KRA_{uuid.uuid4().hex[:8].upper()}"

            # Handle other optional unique fields
            optional_unique_fields = {
                'nssf_number': 'EMPTY_NSSF',
                'shif_number': 'EMPTY_SHIF',
                'email': 'empty_email'
            }

            import uuid
            for field, prefix in optional_unique_fields.items():
                if field in data and (not data[field] or data[field].strip() == ''):
                    if field == 'email':
                        data[field] = f"{prefix}_{uuid.uuid4().hex[:8]}@placeholder.local"
                    else:
                        data[field] = f"{prefix}_{uuid.uuid4().hex[:8].upper()}"

            # Handle other optional fields with empty strings
            optional_fields = ['middle_name', 'address', 'gender', 'marital_status', 'bank_branch', 'bank_code']
            for field in optional_fields:
                if field in data and (not data[field] or data[field].strip() == ''):
                    data[field] = ''

            # Update the form data
            self.data = data

        # Call the parent full_clean with pre-processed data
        super().full_clean()

        # Clear any remaining validation errors for fields we've handled
        if hasattr(self, '_errors') and self._errors:
            fields_to_clear = ['kra_pin', 'nssf_number', 'shif_number', 'middle_name', 'address', 'gender', 'marital_status', 'bank_branch', 'bank_code', 'email']
            for field in fields_to_clear:
                if field in self._errors:
                    # Check if the original input was empty
                    original_value = self.data.get(field, '') if hasattr(self, 'data') else ''
                    if not original_value or original_value.strip() == '' or original_value.startswith('EMPTY_') or original_value.startswith('empty_email_'):
                        # Remove validation errors for fields we've pre-processed
                        del self._errors[field]

    def clean_kra_pin(self):
        """Validate KRA PIN format and uniqueness - OPTIONAL but UNIQUE if provided"""
        kra_pin = self.cleaned_data.get('kra_pin')
        if kra_pin:
            kra_pin = kra_pin.strip().upper()

            # Check format: A123456789B
            if not re.match(r'^[A-Z]\d{9}[A-Z]$', kra_pin):
                raise ValidationError('KRA PIN must be in format: A123456789B')

            # Check uniqueness only if provided
            existing = Employee.objects.filter(kra_pin=kra_pin)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise ValidationError('An employee with this KRA PIN already exists')

        return kra_pin
    
    def clean_phone_number(self):
        """Validate phone number format - OPTIONAL field"""
        phone = self.cleaned_data.get('phone_number')
        if phone:
            # Remove spaces and special characters
            phone = re.sub(r'[^\d+]', '', phone)
            # Check if it's a valid Kenyan number
            if not re.match(r'^(\+254|0)[17]\d{8}$', phone):
                raise ValidationError('Please enter a valid Kenyan phone number')
        return phone
    
    def clean_email(self):
        """Validate email uniqueness"""
        email = self.cleaned_data.get('email')
        if email:
            # Check if email already exists (excluding current instance)
            existing = Employee.objects.filter(email=email)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise ValidationError('An employee with this email already exists')
        # Return None for empty email to store as NULL in database
        return email if email else None

    def clean_account_number(self):
        """Validate bank account number uniqueness - MANDATORY and UNIQUE"""
        account_number = self.cleaned_data.get('account_number')

        # Bank account number is mandatory
        if not account_number:
            raise ValidationError('Bank account number is required and mandatory.')

        account_number = str(account_number).strip()

        if len(account_number) < 6:
            raise ValidationError('Bank account number must be at least 6 characters.')

        # Check uniqueness
        existing = Employee.objects.filter(account_number=account_number)
        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        if existing.exists():
            raise ValidationError('An employee with this bank account number already exists')

        return account_number

    def clean_shif_number(self):
        """Validate SHIF number uniqueness - OPTIONAL but UNIQUE if provided"""
        shif_number = self.cleaned_data.get('shif_number')

        if shif_number:
            shif_number = str(shif_number).strip()

            # Check uniqueness only if provided
            existing = Employee.objects.filter(shif_number=shif_number)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise ValidationError('An employee with this SHIF number already exists')

        return shif_number

    def clean_nssf_number(self):
        """Validate NSSF number uniqueness - OPTIONAL but UNIQUE if provided"""
        nssf_number = self.cleaned_data.get('nssf_number')

        if nssf_number:
            nssf_number = str(nssf_number).strip()

            # Check uniqueness only if provided
            existing = Employee.objects.filter(nssf_number=nssf_number)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise ValidationError('An employee with this NSSF number already exists')

        return nssf_number


class SalaryStructureForm(forms.ModelForm):
    """Form for creating and updating salary structures"""
    
    class Meta:
        model = SalaryStructure
        fields = [
            'employee', 'basic_salary', 'house_allowance', 'transport_allowance',
            'medical_allowance', 'lunch_allowance', 'communication_allowance',
            'other_allowances', 'car_benefit_value', 'housing_benefit_value',
            'life_insurance_premium', 'health_insurance_premium', 
            'education_insurance_premium', 'mortgage_interest',
            'post_retirement_medical_fund', 'pension_contribution',
            'effective_date', 'is_active'
        ]
        widgets = {
            'effective_date': forms.DateInput(attrs={'type': 'date'}),
            'basic_salary': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'house_allowance': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'transport_allowance': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'medical_allowance': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'lunch_allowance': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'communication_allowance': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'other_allowances': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'car_benefit_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'housing_benefit_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'life_insurance_premium': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'health_insurance_premium': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'education_insurance_premium': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'mortgage_interest': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'post_retirement_medical_fund': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'pension_contribution': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
    
    def clean(self):
        """Validate salary structure"""
        cleaned_data = super().clean()
        employee = cleaned_data.get('employee')
        effective_date = cleaned_data.get('effective_date')
        is_active = cleaned_data.get('is_active')
        
        if employee and effective_date and is_active:
            # Check if there's already an active salary structure for this employee
            existing = SalaryStructure.objects.filter(
                employee=employee,
                is_active=True
            )
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise ValidationError(
                    'This employee already has an active salary structure. '
                    'Please deactivate the existing one first.'
                )
        
        return cleaned_data


class DepartmentForm(forms.ModelForm):
    """Form for creating and updating departments"""
    
    class Meta:
        model = Department
        fields = ['name', 'code', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def clean_code(self):
        """Validate department code uniqueness"""
        code = self.cleaned_data.get('code')
        if code:
            code = code.upper()  # Convert to uppercase
            existing = Department.objects.filter(code=code)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise ValidationError('A department with this code already exists')
        return code


class JobTitleForm(forms.ModelForm):
    """Form for creating and updating job titles"""
    
    class Meta:
        model = JobTitle
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def clean_title(self):
        """Validate job title uniqueness"""
        title = self.cleaned_data.get('title')
        if title:
            existing = JobTitle.objects.filter(title__iexact=title)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise ValidationError('A job title with this name already exists')
        return title


class EmployeeSearchForm(forms.Form):
    """Form for searching employees"""
    
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control search-input-large search-input-with-icon',
            'placeholder': 'Search by name, payroll number, email, or KRA PIN...',
            'autocomplete': 'off'
        })
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        empty_label="All Departments",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    employment_type = forms.ChoiceField(
        choices=[('', 'All Types')] + Employee.EMPLOYMENT_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    is_active = forms.ChoiceField(
        choices=[('', 'All'), ('true', 'Active'), ('false', 'Inactive')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class OrganizationForm(forms.ModelForm):
    """Form for creating and editing organizations"""

    class Meta:
        model = Organization
        fields = [
            'organization_type', 'name', 'short_name', 'trading_name',
            'ministry', 'sector', 'address_line_1', 'address_line_2',
            'city', 'postal_code', 'country', 'phone_number', 'email',
            'website', 'kra_pin', 'registration_number', 'registration_authority',
            'nssf_employer_number', 'shif_employer_number', 'logo',
            'default_pay_day', 'is_active'
        ]

        widgets = {
            'organization_type': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Official organization name'}),
            'short_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Acronym (e.g., KRA, MOH)'}),
            'trading_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Trading/business name'}),
            'ministry': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Parent ministry (for government entities)'}),
            'sector': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Industry/sector'}),
            'address_line_1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address line 1'}),
            'address_line_2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address line 2 (optional)'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal code'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+254 XXX XXX XXX'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'info@organization.com'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.organization.com'}),
            'kra_pin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'P123456789A'}),
            'registration_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Registration number'}),
            'registration_authority': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Registration authority'}),
            'nssf_employer_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NSSF employer number'}),
            'shif_employer_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SHIF employer number'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'default_pay_day': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 31}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class BulkEmployeeImportForm(forms.Form):
    """Form for bulk importing employees from Excel file"""
    excel_file = forms.FileField(
        label="Excel File",
        help_text="Upload an Excel file (.xlsx) with employee data. Download the template below for the correct format.",
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx,.xls'
        })
    )

    def process_excel_file(self):
        """Process uploaded Excel file and return employee data"""
        import pandas as pd
        from decimal import Decimal

        excel_file = self.cleaned_data['excel_file']
        errors = []
        employees_data = []

        try:
            # Read Excel file
            df = pd.read_excel(excel_file, sheet_name=0)

            # Required fields
            required_fields = [
                'first_name', 'last_name', 'national_id', 'department',
                'job_title', 'employment_type', 'bank_name', 'account_number'
            ]

            # Check for required columns
            missing_columns = [col for col in required_fields if col not in df.columns]
            if missing_columns:
                errors.append(f"Missing required columns: {', '.join(missing_columns)}")
                return employees_data, errors

            # Process each row
            for index, row in df.iterrows():
                row_num = index + 2  # Excel row number (accounting for header)

                try:
                    # Validate required fields
                    for field in required_fields:
                        if pd.isna(row[field]) or str(row[field]).strip() == '':
                            errors.append(f"Row {row_num}: {field} is required")
                            continue

                    # Get or create department
                    try:
                        department = Department.objects.get(name=str(row['department']).strip())
                    except Department.DoesNotExist:
                        errors.append(f"Row {row_num}: Department '{row['department']}' does not exist")
                        continue

                    # Get or create job title
                    try:
                        job_title = JobTitle.objects.get(title=str(row['job_title']).strip())
                    except JobTitle.DoesNotExist:
                        errors.append(f"Row {row_num}: Job title '{row['job_title']}' does not exist")
                        continue

                    # Validate employment type
                    employment_type = str(row['employment_type']).strip().upper()
                    if employment_type not in ['PERMANENT', 'CONTRACT', 'CASUAL', 'INTERN']:
                        errors.append(f"Row {row_num}: Invalid employment type '{employment_type}'")
                        continue

                    # Validate National ID (8 digits)
                    national_id = str(row['national_id']).strip()
                    if not national_id.isdigit() or len(national_id) != 8:
                        errors.append(f"Row {row_num}: National ID must be exactly 8 digits")
                        continue

                    # Prepare employee data
                    employee_data = {
                        'first_name': str(row['first_name']).strip(),
                        'last_name': str(row['last_name']).strip(),
                        'national_id': national_id,
                        'department': department,
                        'job_title': job_title,
                        'employment_type': employment_type,
                        'bank_name': str(row['bank_name']).strip(),
                        'account_number': str(row['account_number']).strip(),
                    }

                    # Optional fields
                    optional_fields = {
                        'middle_name': 'middle_name',
                        'phone_number': 'phone_number',
                        'email': 'email',
                        'gender': 'gender',
                        'address': 'address',
                        'kra_pin': 'kra_pin',
                        'nssf_number': 'nssf_number',
                        'shif_number': 'shif_number',
                        'bank_code': 'bank_code',
                        'bank_branch': 'bank_branch',
                    }

                    for excel_field, model_field in optional_fields.items():
                        if excel_field in df.columns and not pd.isna(row[excel_field]):
                            value = str(row[excel_field]).strip()
                            if value:
                                employee_data[model_field] = value

                    # Handle date fields
                    date_fields = ['date_of_birth', 'date_hired']
                    for field in date_fields:
                        if field in df.columns and not pd.isna(row[field]):
                            try:
                                if isinstance(row[field], str):
                                    from datetime import datetime
                                    date_value = datetime.strptime(row[field], '%Y-%m-%d').date()
                                else:
                                    date_value = row[field].date() if hasattr(row[field], 'date') else row[field]
                                employee_data[field] = date_value
                            except (ValueError, AttributeError):
                                errors.append(f"Row {row_num}: Invalid date format for {field}")

                    employees_data.append(employee_data)

                except Exception as e:
                    errors.append(f"Row {row_num}: Error processing row - {str(e)}")

        except Exception as e:
            errors.append(f"Error reading Excel file: {str(e)}")

        return employees_data, errors

# Original class commented out:
# class BulkEmployeeImportForm(forms.Form):
#     """Form for bulk importing employees from Excel file"""
#     excel_file = forms.FileField(
#         label="Excel File",
#         help_text="Upload an Excel file (.xlsx) with employee data. Download the template below for the correct format.",
#         widget=forms.FileInput(attrs={
#             'class': 'form-control',
#             'accept': '.xlsx,.xls'
#         })
#     )

#     def clean_excel_file(self):
#         """Validate the uploaded Excel file"""
#         excel_file = self.cleaned_data.get('excel_file')
#
#         if not excel_file:
#             raise ValidationError('Please select an Excel file to upload.')
#
#         # Check file extension
#         if not excel_file.name.lower().endswith(('.xlsx', '.xls')):
#             raise ValidationError('Please upload a valid Excel file (.xlsx or .xls).')
#
#         # Check file size (limit to 10MB)
#         if excel_file.size > 10 * 1024 * 1024:
#             raise ValidationError('File size must be less than 10MB.')
#
#         return excel_file
#
#     def process_excel_file(self):
#         """Process the Excel file and return employee data"""
class EmployeeValidationMixin:
    """Mixin for employee form validation"""

    def clean_kra_pin(self):
        kra_pin = self.cleaned_data.get('kra_pin')
        if kra_pin:
            # Validate KRA PIN format
            if not re.match(r'^P\d{9}[A-Z]$', kra_pin):
                raise ValidationError('KRA PIN must be in format: P123456789A')
        return kra_pin
