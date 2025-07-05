# Generated migration for adding payroll_number field

from django.db import migrations, models


def assign_payroll_numbers(apps, schema_editor):
    """Assign unique payroll numbers to existing employees"""
    Employee = apps.get_model('employees', 'Employee')
    employees = Employee.objects.all().order_by('id')
    
    for index, employee in enumerate(employees, start=1):
        employee.payroll_number = f"PAY{index:04d}"
        employee.save()


def reverse_payroll_numbers(apps, schema_editor):
    """Reverse operation - remove payroll numbers"""
    pass  # No reverse needed for adding field


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0005_make_email_optional'),
    ]

    operations = [
        # Add the new field as nullable first
        migrations.AddField(
            model_name='employee',
            name='payroll_number',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        
        # Assign unique payroll numbers to existing employees
        migrations.RunPython(assign_payroll_numbers, reverse_payroll_numbers),
        
        # Make the field non-nullable and unique
        migrations.AlterField(
            model_name='employee',
            name='payroll_number',
            field=models.CharField(max_length=20, unique=True, editable=False),
        ),
    ]
