from django.contrib import admin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.urls import path
from django import forms
from .models import Department, JobTitle, Employee, SalaryStructure, Organization
import openpyxl
import pandas as pd
import io
from datetime import datetime
from decimal import Decimal


class BulkImportForm(forms.Form):
    """Form for bulk importing employees"""
    file = forms.FileField(
        label="Upload File",
        help_text="Upload Excel (.xlsx, .xls) or CSV file with employee data",
        widget=forms.FileInput(attrs={
            'accept': '.xlsx,.xls,.csv',
            'class': 'form-control'
        })
    )


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization_type', 'short_name', 'ministry', 'sector', 'city', 'is_active']
    list_filter = ['organization_type', 'is_active', 'country', 'city', 'sector']
    search_fields = ['name', 'short_name', 'trading_name', 'kra_pin', 'registration_number', 'ministry']
    fieldsets = (
        ('Basic Information', {
            'fields': ('organization_type', 'name', 'short_name', 'trading_name', 'is_active')
        }),
        ('Organizational Structure', {
            'fields': ('ministry', 'sector'),
            'description': 'For government entities, specify the parent ministry and sector'
        }),
        ('Contact Information', {
            'fields': ('address_line_1', 'address_line_2', 'city', 'postal_code', 'country', 'phone_number', 'email', 'website')
        }),
        ('Registration & Compliance', {
            'fields': ('kra_pin', 'registration_number', 'registration_authority', 'nssf_employer_number', 'shif_employer_number')
        }),
        ('Payroll Settings', {
            'fields': ('default_pay_day', 'logo')
        }),
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'organization', 'organization_type', 'created_at']
    list_filter = ['organization', 'organization__organization_type', 'created_at']
    search_fields = ['name', 'code', 'organization__name', 'organization__short_name']
    ordering = ['organization__name', 'name']

    def organization_type(self, obj):
        return obj.organization.get_organization_type_display()
    organization_type.short_description = 'Organization Type'


@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title']
    ordering = ['title']


class SalaryStructureInline(admin.StackedInline):
    model = SalaryStructure
    extra = 0


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        'payroll_number', 'full_name', 'department', 'job_title',
        'employment_type', 'date_hired', 'is_active'
    ]
    list_filter = [
        'department', 'job_title', 'employment_type', 'is_active',
        'gender', 'marital_status', 'date_hired'
    ]
    search_fields = [
        'payroll_number', 'first_name', 'last_name', 'email',
        'national_id', 'kra_pin', 'nssf_number', 'shif_number'
    ]
    ordering = ['payroll_number']

    # Exclude payroll_number from forms since it's auto-generated
    exclude = ['payroll_number']

    fieldsets = (
        ('Personal Information', {
            'fields': (
                'first_name', 'middle_name', 'last_name',
                'date_of_birth', 'gender', 'marital_status', 'national_id'
            )
        }),
        ('Contact Information', {
            'fields': ('email', 'phone_number', 'address')
        }),
        ('Employment Information', {
            'fields': (
                'department', 'job_title', 'employment_type',
                'date_hired', 'date_terminated', 'is_active'
            )
        }),
        ('Statutory Information', {
            'fields': ('kra_pin', 'nssf_number', 'shif_number')
        }),
        ('Banking Information', {
            'fields': ('bank_name', 'bank_branch', 'account_number')
        }),
        ('System Information', {
            'fields': ('user',),
            'classes': ('collapse',)
        })
    )

    def get_readonly_fields(self, request, obj=None):
        """Return readonly fields - payroll_number only for existing employees"""
        if obj:  # Editing existing employee - show payroll_number as readonly
            return ['payroll_number']
        return []  # No readonly fields when adding new employee

    def get_exclude(self, request, obj=None):
        """Exclude payroll_number from add form, but show it in edit form"""
        if not obj:  # Adding new employee
            return ['payroll_number']
        return []  # Don't exclude anything when editing existing employee

    def get_fieldsets(self, request, obj=None):
        """Return different fieldsets for add vs change forms"""
        if obj:  # Editing existing employee - include payroll_number
            return (
                ('Personal Information', {
                    'fields': (
                        'payroll_number', 'first_name', 'middle_name', 'last_name',
                        'date_of_birth', 'gender', 'marital_status', 'national_id'
                    )
                }),
                ('Contact Information', {
                    'fields': ('email', 'phone_number', 'address')
                }),
                ('Employment Information', {
                    'fields': (
                        'department', 'job_title', 'employment_type',
                        'date_hired', 'date_terminated', 'is_active'
                    )
                }),
                ('Statutory Information', {
                    'fields': ('kra_pin', 'nssf_number', 'shif_number')
                }),
                ('Banking Information', {
                    'fields': ('bank_name', 'bank_branch', 'account_number')
                }),
                ('System Information', {
                    'fields': ('user',),
                    'classes': ('collapse',)
                })
            )
        return super().get_fieldsets(request, obj)  # Use default fieldsets for add form

    inlines = [SalaryStructureInline]
    actions = ['bulk_import_employees']

    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Full Name'

    def get_urls(self):
        """Add custom URLs for bulk import"""
        urls = super().get_urls()
        custom_urls = [
            path('bulk-import/', self.admin_site.admin_view(self.bulk_import_view), name='employees_employee_bulk_import'),
            path('download-template/', self.admin_site.admin_view(self.download_template), name='employees_employee_download_template'),
        ]
        return custom_urls + urls

    def bulk_import_employees(self, request, queryset):
        """Admin action to redirect to bulk import page"""
        return redirect('admin:employees_employee_bulk_import')
    bulk_import_employees.short_description = "Bulk Import Employees from File"

    def bulk_import_view(self, request):
        """Handle bulk import of employees"""
        if request.method == 'POST':
            form = BulkImportForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    file = form.cleaned_data['file']
                    file_extension = file.name.split('.')[-1].lower()

                    if file_extension in ['xlsx', 'xls']:
                        result = self._process_excel_file(file)
                    elif file_extension == 'csv':
                        result = self._process_csv_file(file)
                    else:
                        messages.error(request, 'Unsupported file format. Please upload Excel (.xlsx, .xls) or CSV file.')
                        return render(request, 'admin/employees/employee/bulk_import.html', {'form': form})

                    success_count, errors = result

                    if success_count > 0:
                        messages.success(request, f'Successfully imported {success_count} employees!')

                    if errors:
                        for error in errors[:10]:  # Show first 10 errors
                            messages.error(request, error)
                        if len(errors) > 10:
                            messages.warning(request, f'... and {len(errors) - 10} more errors.')

                    return redirect('admin:employees_employee_changelist')

                except Exception as e:
                    messages.error(request, f'Error processing file: {str(e)}')
        else:
            form = BulkImportForm()

        return render(request, 'admin/employees/employee/bulk_import.html', {
            'form': form,
            'title': 'Bulk Import Employees',
            'opts': self.model._meta,
        })

    def _process_excel_file(self, file):
        """Process Excel file and create employees"""
        success_count = 0
        errors = []

        try:
            # Read Excel file
            df = pd.read_excel(file)

            # Process each row
            for index, row in df.iterrows():
                try:
                    employee_data = self._extract_employee_data(row, index + 2)  # +2 for header and 0-based index
                    if employee_data:
                        employee = Employee.objects.create(**employee_data)
                        success_count += 1
                except Exception as e:
                    errors.append(f'Row {index + 2}: {str(e)}')

        except Exception as e:
            errors.append(f'Error reading Excel file: {str(e)}')

        return success_count, errors

    def _process_csv_file(self, file):
        """Process CSV file and create employees"""
        success_count = 0
        errors = []

        try:
            # Read CSV file
            df = pd.read_csv(file)

            # Process each row
            for index, row in df.iterrows():
                try:
                    employee_data = self._extract_employee_data(row, index + 2)  # +2 for header and 0-based index
                    if employee_data:
                        employee = Employee.objects.create(**employee_data)
                        success_count += 1
                except Exception as e:
                    errors.append(f'Row {index + 2}: {str(e)}')

        except Exception as e:
            errors.append(f'Error reading CSV file: {str(e)}')

        return success_count, errors

    def _extract_employee_data(self, row, row_number):
        """Extract and validate employee data from a row"""
        try:
            # Required fields
            first_name = str(row.get('first_name', '')).strip()
            last_name = str(row.get('last_name', '')).strip()

            if not first_name or not last_name:
                raise ValueError('First name and last name are required')

            # Get or create department and job title
            department_name = str(row.get('department', '')).strip()
            job_title_name = str(row.get('job_title', '')).strip()

            if not department_name:
                raise ValueError('Department is required')
            if not job_title_name:
                raise ValueError('Job title is required')

            # Get first active organization (or create default)
            organization = Organization.objects.filter(is_active=True).first()
            if not organization:
                raise ValueError('No active organization found. Please create an organization first.')

            # Get or create department
            department, created = Department.objects.get_or_create(
                name=department_name,
                organization=organization,
                defaults={'code': department_name[:10].upper()}
            )

            # Get or create job title
            job_title, created = JobTitle.objects.get_or_create(
                title=job_title_name
            )

            # Prepare employee data
            employee_data = {
                'first_name': first_name,
                'last_name': last_name,
                'department': department,
                'job_title': job_title,
                'employment_type': str(row.get('employment_type', 'PERMANENT')).upper(),
                'is_active': True,
            }

            # Optional fields
            middle_name = str(row.get('middle_name', '')).strip()
            if middle_name and middle_name.lower() != 'nan':
                employee_data['middle_name'] = middle_name

            email = str(row.get('email', '')).strip()
            if email and email.lower() != 'nan' and '@' in email:
                employee_data['email'] = email

            phone_number = str(row.get('phone_number', '')).strip()
            if phone_number and phone_number.lower() != 'nan':
                employee_data['phone_number'] = phone_number

            national_id = str(row.get('national_id', '')).strip()
            if national_id and national_id.lower() != 'nan':
                # Check if employee with this National ID already exists
                if Employee.objects.filter(national_id=national_id).exists():
                    raise ValueError(f'Employee with National ID {national_id} already exists')
                employee_data['national_id'] = national_id

            address = str(row.get('address', '')).strip()
            if address and address.lower() != 'nan':
                employee_data['address'] = address

            gender = str(row.get('gender', '')).strip().upper()
            if gender and gender in ['M', 'F', 'O']:
                employee_data['gender'] = gender

            marital_status = str(row.get('marital_status', '')).strip().upper()
            if marital_status and marital_status in ['SINGLE', 'MARRIED', 'DIVORCED', 'WIDOWED']:
                employee_data['marital_status'] = marital_status

            # Date fields
            date_of_birth = row.get('date_of_birth')
            if pd.notna(date_of_birth):
                if isinstance(date_of_birth, str):
                    try:
                        employee_data['date_of_birth'] = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
                    except ValueError:
                        try:
                            employee_data['date_of_birth'] = datetime.strptime(date_of_birth, '%d/%m/%Y').date()
                        except ValueError:
                            pass
                else:
                    employee_data['date_of_birth'] = date_of_birth

            date_hired = row.get('date_hired')
            if pd.notna(date_hired):
                if isinstance(date_hired, str):
                    try:
                        employee_data['date_hired'] = datetime.strptime(date_hired, '%Y-%m-%d').date()
                    except ValueError:
                        try:
                            employee_data['date_hired'] = datetime.strptime(date_hired, '%d/%m/%Y').date()
                        except ValueError:
                            pass
                else:
                    employee_data['date_hired'] = date_hired

            # Statutory information
            kra_pin = str(row.get('kra_pin', '')).strip()
            if kra_pin and kra_pin.lower() != 'nan':
                employee_data['kra_pin'] = kra_pin

            nssf_number = str(row.get('nssf_number', '')).strip()
            if nssf_number and nssf_number.lower() != 'nan':
                employee_data['nssf_number'] = nssf_number

            shif_number = str(row.get('shif_number', '')).strip()
            if shif_number and shif_number.lower() != 'nan':
                employee_data['shif_number'] = shif_number

            # Banking information
            bank_name = str(row.get('bank_name', '')).strip()
            if bank_name and bank_name.lower() != 'nan':
                employee_data['bank_name'] = bank_name

            bank_branch = str(row.get('bank_branch', '')).strip()
            if bank_branch and bank_branch.lower() != 'nan':
                employee_data['bank_branch'] = bank_branch

            account_number = str(row.get('account_number', '')).strip()
            if account_number and account_number.lower() != 'nan':
                employee_data['account_number'] = account_number

            return employee_data

        except Exception as e:
            raise ValueError(f'Error processing row data: {str(e)}')

    def download_template(self, request):
        """Download Excel template for bulk import"""
        # Create workbook
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Employee_Template"

        # Headers
        headers = [
            'first_name', 'middle_name', 'last_name', 'email', 'phone_number',
            'national_id', 'address', 'gender', 'marital_status', 'date_of_birth',
            'department', 'job_title', 'employment_type', 'date_hired',
            'kra_pin', 'nssf_number', 'shif_number',
            'bank_name', 'bank_branch', 'account_number'
        ]

        # Add headers
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = openpyxl.styles.Font(bold=True)
            cell.fill = openpyxl.styles.PatternFill(start_color="CCCCCC", end_color="CCCCCC", fill_type="solid")

        # Add sample data
        sample_data = [
            'John', 'Doe', 'Smith', 'john.smith@example.com', '+254712345678',
            '12345678', '123 Main St, Nairobi', 'M', 'SINGLE', '1990-01-15',
            'IT Department', 'Software Developer', 'PERMANENT', '2024-01-01',
            'A123456789B', '1234567890', 'SHIF123456',
            'KCB Bank', 'Nairobi Branch', '1234567890'
        ]

        for col, value in enumerate(sample_data, 1):
            ws.cell(row=2, column=col, value=value)

        # Add instructions sheet
        instructions_ws = wb.create_sheet("Instructions")
        instructions = [
            "EMPLOYEE BULK IMPORT TEMPLATE INSTRUCTIONS",
            "",
            "REQUIRED FIELDS (must be provided):",
            "- first_name: Employee's first name",
            "- last_name: Employee's last name",
            "- department: Department name (will be created if doesn't exist)",
            "- job_title: Job title (will be created if doesn't exist)",
            "",
            "OPTIONAL FIELDS:",
            "- middle_name: Employee's middle name",
            "- email: Valid email address",
            "- phone_number: Phone number (e.g., +254712345678)",
            "- national_id: National ID number",
            "- address: Physical address",
            "- gender: M (Male), F (Female), O (Other)",
            "- marital_status: SINGLE, MARRIED, DIVORCED, WIDOWED",
            "- date_of_birth: Format: YYYY-MM-DD or DD/MM/YYYY",
            "- employment_type: PERMANENT, CONTRACT, CASUAL, INTERN",
            "- date_hired: Format: YYYY-MM-DD or DD/MM/YYYY",
            "- kra_pin: KRA PIN (format: A123456789B)",
            "- nssf_number: NSSF number",
            "- shif_number: SHIF number",
            "- bank_name: Bank name",
            "- bank_branch: Bank branch",
            "- account_number: Bank account number",
            "",
            "NOTES:",
            "- Empty cells for optional fields will be ignored",
            "- Duplicate National IDs will be rejected",
            "- Invalid data formats will cause import errors",
            "- Departments and job titles will be created automatically if they don't exist"
        ]

        for row, instruction in enumerate(instructions, 1):
            instructions_ws.cell(row=row, column=1, value=instruction)

        # Adjust column widths
        for ws_sheet in [ws, instructions_ws]:
            for column in ws_sheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                ws_sheet.column_dimensions[column_letter].width = adjusted_width

        # Create response
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="employee_bulk_import_template.xlsx"'

        # Save workbook to response
        wb.save(response)
        return response


@admin.register(SalaryStructure)
class SalaryStructureAdmin(admin.ModelAdmin):
    list_display = [
        'employee', 'basic_salary', 'gross_salary', 'effective_date', 'is_active'
    ]
    list_filter = ['is_active', 'effective_date']
    search_fields = ['employee__first_name', 'employee__last_name', 'employee__employee_number']
    ordering = ['-effective_date']

    fieldsets = (
        ('Employee', {
            'fields': ('employee', 'effective_date', 'is_active')
        }),
        ('Basic Salary', {
            'fields': ('basic_salary',)
        }),
        ('Allowances', {
            'fields': (
                'house_allowance', 'transport_allowance', 'medical_allowance',
                'lunch_allowance', 'communication_allowance', 'other_allowances'
            )
        }),
        ('Benefits (Non-Cash)', {
            'fields': ('car_benefit_value', 'housing_benefit_value')
        }),
        ('Insurance & Pension', {
            'fields': (
                'life_insurance_premium', 'health_insurance_premium',
                'education_insurance_premium', 'pension_contribution'
            )
        }),
        ('Tax Relief Items', {
            'fields': ('mortgage_interest', 'post_retirement_medical_fund')
        }),
    )
