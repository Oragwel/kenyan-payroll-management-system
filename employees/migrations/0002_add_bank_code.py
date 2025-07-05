# Generated manually to add bank_code field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='bank_code',
            field=models.CharField(
                blank=True, 
                choices=[
                    ('12053', '12053'),
                    ('68058', '68058'),
                    ('01169', '01169'),
                    ('11081', '11081'),
                    ('03017', '03017'),
                    ('74004', '74004'),
                    ('72006', '72006')
                ],
                max_length=10, 
                null=True
            ),
        ),
    ]
