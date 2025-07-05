# Generated manually to make statutory fields optional

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0004_make_gender_optional'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='kra_pin',
            field=models.CharField(blank=True, help_text='KRA PIN in format: A123456789B (Optional)', max_length=11, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='KRA PIN must be in format: A123456789B', regex='^[A-Z]\\d{9}[A-Z]$')]),
        ),
        migrations.AlterField(
            model_name='employee',
            name='nssf_number',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='shif_number',
            field=models.CharField(blank=True, help_text='SHIF membership number (Social Health Insurance Fund)', max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='bank_branch',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='marital_status',
            field=models.CharField(blank=True, choices=[('SINGLE', 'Single'), ('MARRIED', 'Married'), ('DIVORCED', 'Divorced'), ('WIDOWED', 'Widowed')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='middle_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
    ]
