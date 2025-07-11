# Generated by Django 3.1.14 on 2025-07-04 07:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employees', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PayrollPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('period_type', models.CharField(choices=[('MONTHLY', 'Monthly'), ('WEEKLY', 'Weekly'), ('BIWEEKLY', 'Bi-weekly')], default='MONTHLY', max_length=10)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('pay_date', models.DateField()),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('PROCESSING', 'Processing'), ('COMPLETED', 'Completed'), ('APPROVED', 'Approved'), ('PAID', 'Paid')], default='DRAFT', max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='approved_payroll_periods', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_payroll_periods', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-start_date'],
                'unique_together': {('start_date', 'end_date', 'period_type')},
            },
        ),
        migrations.CreateModel(
            name='PayrollSummary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_employees', models.IntegerField(default=0)),
                ('active_employees', models.IntegerField(default=0)),
                ('total_gross_pay', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('total_basic_salary', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('total_allowances', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('total_benefits', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('total_paye', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('total_nssf_employee', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('total_nssf_employer', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('total_nhif', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('total_shif', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('total_housing_levy_employee', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('total_housing_levy_employer', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('total_other_deductions', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('total_deductions', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('total_net_pay', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('total_personal_relief', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('total_insurance_relief', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('total_mortgage_relief', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('total_pension_relief', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('payroll_period', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='summary', to='payroll_processing.payrollperiod')),
            ],
            options={
                'ordering': ['-payroll_period__start_date'],
            },
        ),
        migrations.CreateModel(
            name='Payslip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basic_salary', models.DecimalField(decimal_places=2, max_digits=12)),
                ('house_allowance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('transport_allowance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('medical_allowance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('lunch_allowance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('communication_allowance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('other_allowances', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('overtime_pay', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('bonus', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('car_benefit', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('housing_benefit', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('other_benefits', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('gross_pay', models.DecimalField(decimal_places=2, max_digits=12)),
                ('paye_tax', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('nssf_employee', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('nhif_contribution', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('shif_contribution', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('housing_levy_employee', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('loan_deductions', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('advance_deductions', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('other_deductions', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('total_deductions', models.DecimalField(decimal_places=2, max_digits=12)),
                ('net_pay', models.DecimalField(decimal_places=2, max_digits=12)),
                ('nssf_employer', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('housing_levy_employer', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('personal_relief', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('insurance_relief', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('mortgage_relief', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('pension_relief', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payslips', to='employees.employee')),
                ('payroll_period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payslips', to='payroll_processing.payrollperiod')),
            ],
            options={
                'ordering': ['-payroll_period__start_date', 'employee__employee_number'],
                'unique_together': {('payroll_period', 'employee')},
            },
        ),
    ]
