from django.contrib import admin
from .models import Department, JobTitle, Employee, SalaryStructure, Organization


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

    fieldsets = (
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

    inlines = [SalaryStructureInline]

    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Full Name'


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
