from django.core.management.base import BaseCommand
from employees.models import Organization, Department


class Command(BaseCommand):
    help = 'Add Municipality department to all active organizations'

    def handle(self, *args, **options):
        self.stdout.write("🏛️ Adding Municipality Department to Organizations...")
        
        # Get all active organizations
        organizations = Organization.objects.filter(is_active=True)
        
        if not organizations.exists():
            self.stdout.write(self.style.ERROR("❌ No active organizations found"))
            return
        
        added_count = 0
        existing_count = 0
        
        for organization in organizations:
            self.stdout.write(f"\n📋 Processing organization: {organization.name}")
            
            # Check if Municipality department already exists
            municipality_dept = Department.objects.filter(
                organization=organization,
                name='Municipality'
            ).first()
            
            if municipality_dept:
                self.stdout.write(f"   ℹ️  Municipality department already exists: {municipality_dept.name} ({municipality_dept.code})")
                existing_count += 1
            else:
                # Create Municipality department
                municipality_dept = Department.objects.create(
                    organization=organization,
                    name='Municipality',
                    code='MUNIC',
                    description='Municipality Department'
                )
                self.stdout.write(self.style.SUCCESS(f"   ✅ Created Municipality department: {municipality_dept.name} ({municipality_dept.code})"))
                added_count += 1
        
        self.stdout.write(f"\n🎯 Summary:")
        self.stdout.write(f"   Organizations processed: {organizations.count()}")
        self.stdout.write(f"   Municipality departments added: {added_count}")
        self.stdout.write(f"   Municipality departments already existing: {existing_count}")
        
        # Show all departments for each organization
        for organization in organizations:
            departments = Department.objects.filter(organization=organization).order_by('name')
            self.stdout.write(f"\n📋 {organization.name} - Departments ({departments.count()}):")
            for dept in departments:
                self.stdout.write(f"   • {dept.name} ({dept.code})")
        
        self.stdout.write(self.style.SUCCESS("\n✅ Municipality department addition completed!"))
