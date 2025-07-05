from django.contrib import admin
from .models import PayrollPeriod, Payslip, PayrollSummary


@admin.register(PayrollPeriod)
class PayrollPeriodAdmin(admin.ModelAdmin):
    list_display = ['name', 'period_type', 'start_date', 'end_date', 'pay_date', 'status', 'created_by']
    list_filter = ['period_type', 'status', 'start_date']
    search_fields = ['name']
    ordering = ['-start_date']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Payslip)
class PayslipAdmin(admin.ModelAdmin):
    list_display = ['employee', 'payroll_period', 'gross_pay', 'total_deductions', 'net_pay']
    list_filter = ['payroll_period', 'payroll_period__status']
    search_fields = ['employee__first_name', 'employee__last_name', 'employee__payroll_number']
    ordering = ['-payroll_period__start_date', 'employee__payroll_number']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(PayrollSummary)
class PayrollSummaryAdmin(admin.ModelAdmin):
    list_display = ['payroll_period', 'total_employees', 'total_gross_pay', 'total_net_pay']
    list_filter = ['payroll_period__status', 'payroll_period__start_date']
    ordering = ['-payroll_period__start_date']
    readonly_fields = ['created_at', 'updated_at']
