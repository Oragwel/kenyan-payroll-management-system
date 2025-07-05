# Generated migration for removing employee_number field

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0006_add_payroll_number_field'),
    ]

    operations = [
        # Remove the old field
        migrations.RemoveField(
            model_name='employee',
            name='employee_number',
        ),
        
        # Update Meta options
        migrations.AlterModelOptions(
            name='employee',
            options={'ordering': ['payroll_number']},
        ),
    ]
