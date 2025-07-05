# Generated manually to make gender field optional

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0003_make_bank_branch_optional'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1, null=True),
        ),
    ]
