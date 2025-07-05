# Generated manually to make bank_branch field optional

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_add_bank_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='bank_branch',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
