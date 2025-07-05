# Generated migration for adding Ugatuzi department and Casual Worker job title

from django.db import migrations


def add_ugatuzi_and_casual_worker(apps, schema_editor):
    """Add Ugatuzi department and Casual Worker job title"""
    Department = apps.get_model('employees', 'Department')
    JobTitle = apps.get_model('employees', 'JobTitle')
    
    # Add Ugatuzi department if it doesn't exist
    ugatuzi_dept, created = Department.objects.get_or_create(
        name='Ugatuzi',
        defaults={
            'code': 'UGA',
            'description': 'Ugatuzi Department - General Services and Support'
        }
    )
    
    # Add Casual Worker job title if it doesn't exist
    casual_worker, created = JobTitle.objects.get_or_create(
        title='Casual Worker',
        defaults={
            'description': 'Temporary or casual employment position'
        }
    )


def reverse_ugatuzi_and_casual_worker(apps, schema_editor):
    """Remove Ugatuzi department and Casual Worker job title"""
    Department = apps.get_model('employees', 'Department')
    JobTitle = apps.get_model('employees', 'JobTitle')
    
    # Remove if no employees are assigned
    try:
        ugatuzi_dept = Department.objects.get(name='Ugatuzi')
        if not ugatuzi_dept.employee_set.exists():
            ugatuzi_dept.delete()
    except Department.DoesNotExist:
        pass
    
    try:
        casual_worker = JobTitle.objects.get(title='Casual Worker')
        if not casual_worker.employee_set.exists():
            casual_worker.delete()
    except JobTitle.DoesNotExist:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0007_remove_employee_number_field'),
    ]

    operations = [
        migrations.RunPython(add_ugatuzi_and_casual_worker, reverse_ugatuzi_and_casual_worker),
    ]
