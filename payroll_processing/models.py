from django.db import models
from django.contrib.auth.models import User
from employees.models import Employee


class PayrollPeriod(models.Model):
    """Payroll periods for processing salaries"""
    PERIOD_TYPE_CHOICES = [
        ('MONTHLY', 'Monthly'),
        ('WEEKLY', 'Weekly'),
        ('BIWEEKLY', 'Bi-weekly'),
    ]

    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('APPROVED', 'Approved'),
        ('PAID', 'Paid'),
    ]

    name = models.CharField(max_length=100)
    period_type = models.CharField(max_length=10, choices=PERIOD_TYPE_CHOICES, default='MONTHLY')
    start_date = models.DateField()
    end_date = models.DateField()
    pay_date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='DRAFT')

    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_payroll_periods')
    approved_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='approved_payroll_periods')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.start_date} to {self.end_date})"

    class Meta:
        ordering = ['-start_date']
        unique_together = ['start_date', 'end_date', 'period_type']


class Payslip(models.Model):
    """Individual employee payslip for a payroll period"""
    payroll_period = models.ForeignKey(PayrollPeriod, on_delete=models.CASCADE, related_name='payslips')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payslips')

    # Earnings
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2)
    house_allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    transport_allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    medical_allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    lunch_allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    communication_allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other_allowances = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    overtime_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bonus = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Benefits (taxable)
    car_benefit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    housing_benefit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other_benefits = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Gross Pay
    gross_pay = models.DecimalField(max_digits=12, decimal_places=2)

    # Statutory Deductions
    paye_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    nssf_employee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    shif_contribution = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    housing_levy_employee = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Other Deductions
    loan_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    advance_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Total Deductions
    total_deductions = models.DecimalField(max_digits=12, decimal_places=2)

    # Net Pay
    net_pay = models.DecimalField(max_digits=12, decimal_places=2)

    # Employer Contributions
    nssf_employer = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    housing_levy_employer = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Tax Relief Applied
    personal_relief = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    insurance_relief = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    mortgage_relief = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pension_relief = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payslip for {self.employee.full_name} - {self.payroll_period.name}"

    @property
    def total_allowances(self):
        """Calculate total allowances (excluding basic salary)"""
        return (
            self.house_allowance +
            self.transport_allowance +
            self.medical_allowance +
            self.lunch_allowance +
            self.communication_allowance +
            self.other_allowances +
            self.overtime_pay +
            self.bonus
        )

    @property
    def total_benefits(self):
        """Calculate total benefits"""
        return (
            self.car_benefit +
            self.housing_benefit +
            self.other_benefits
        )

    @property
    def total_earnings(self):
        """Calculate total earnings before deductions"""
        return (
            self.basic_salary +
            self.total_allowances +
            self.total_benefits
        )

    @property
    def total_statutory_deductions(self):
        """Calculate total statutory deductions"""
        return (
            self.paye_tax +
            self.nssf_employee +
            self.shif_contribution +
            self.housing_levy_employee
        )

    @property
    def total_other_deductions(self):
        """Calculate total other deductions"""
        return (
            self.loan_deductions +
            self.advance_deductions +
            self.other_deductions
        )

    class Meta:
        ordering = ['-payroll_period__start_date', 'employee__payroll_number']
        unique_together = ['payroll_period', 'employee']


class PayrollSummary(models.Model):
    """Summary of payroll for a period"""
    payroll_period = models.OneToOneField(PayrollPeriod, on_delete=models.CASCADE, related_name='summary')

    # Employee counts
    total_employees = models.IntegerField(default=0)
    active_employees = models.IntegerField(default=0)

    # Financial totals
    total_gross_pay = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_basic_salary = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_allowances = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_benefits = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    # Total deductions
    total_paye = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_nssf_employee = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_nssf_employer = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_shif = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_housing_levy_employee = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_housing_levy_employer = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_other_deductions = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    # Net totals
    total_deductions = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_net_pay = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    # Tax relief totals
    total_personal_relief = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_insurance_relief = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_mortgage_relief = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_pension_relief = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payroll Summary for {self.payroll_period.name}"

    class Meta:
        ordering = ['-payroll_period__start_date']
