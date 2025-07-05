from django.core.management.base import BaseCommand
from employees.models import Organization, Department


class Command(BaseCommand):
    help = 'Create sample organizations and departments for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            type=str,
            default='company',
            choices=['company', 'government', 'all'],
            help='Type of organization to create'
        )

    def handle(self, *args, **options):
        org_type = options['type']

        if org_type in ['company', 'all']:
            self.create_company()

        if org_type in ['government', 'all']:
            self.create_government_entities()

    def create_company(self):
        """Create sample private company"""
        company, created = Organization.objects.get_or_create(
            name="Kenyan Tech Solutions Ltd",
            defaults={
                'organization_type': 'COMPANY',
                'short_name': 'KTS',
                'trading_name': "KTS Ltd",
                'sector': 'Information Technology',
                'address_line_1': "Westlands Business Park",
                'address_line_2': "Ring Road Westlands",
                'city': "Nairobi",
                'postal_code': "00100",
                'country': "Kenya",
                'phone_number': "+254 20 123 4567",
                'email': "info@kenyantechsolutions.co.ke",
                'website': "https://www.kenyantechsolutions.co.ke",
                'kra_pin': "P051234567A",
                'registration_number': "CPR/2020/123456",
                'registration_authority': "Registrar of Companies",
                'nssf_employer_number': "EMP001234",
                'shif_employer_number': "SHF001234",
                'default_pay_day': 25,
                'is_active': True,
            }
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created company: {company.name}')
            )
            self.create_company_departments(company)
        else:
            self.stdout.write(
                self.style.WARNING(f'Company already exists: {company.name}')
            )

    def create_government_entities(self):
        """Create sample government entities"""
        # Ministry of Health
        moh, created = Organization.objects.get_or_create(
            name="Ministry of Health",
            defaults={
                'organization_type': 'GOVERNMENT',
                'short_name': 'MOH',
                'sector': 'Health',
                'address_line_1': "Afya House",
                'address_line_2': "Cathedral Road",
                'city': "Nairobi",
                'postal_code': "00100",
                'country': "Kenya",
                'phone_number': "+254 20 271 7077",
                'email': "info@health.go.ke",
                'website': "https://www.health.go.ke",
                'kra_pin': "P051234568B",
                'registration_number': "GOV/MOH/2010",
                'registration_authority': "Government of Kenya",
                'nssf_employer_number': "GOV001234",
                'shif_employer_number': "GOV001234",
                'default_pay_day': 28,
                'is_active': True,
            }
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created ministry: {moh.name}')
            )
            self.create_government_departments(moh)

        # Kenya Revenue Authority (Parastatal)
        kra, created = Organization.objects.get_or_create(
            name="Kenya Revenue Authority",
            defaults={
                'organization_type': 'PARASTATAL',
                'short_name': 'KRA',
                'ministry': 'National Treasury and Economic Planning',
                'sector': 'Revenue Collection',
                'address_line_1': "Times Tower",
                'address_line_2': "Haile Selassie Avenue",
                'city': "Nairobi",
                'postal_code': "00100",
                'country': "Kenya",
                'phone_number': "+254 20 281 7000",
                'email': "info@kra.go.ke",
                'website': "https://www.kra.go.ke",
                'kra_pin': "P051234569C",
                'registration_number': "KRA/1995/001",
                'registration_authority': "Government of Kenya",
                'nssf_employer_number': "KRA001234",
                'shif_employer_number': "KRA001234",
                'default_pay_day': 28,
                'is_active': True,
            }
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created parastatal: {kra.name}')
            )
            self.create_kra_departments(kra)

    def create_company_departments(self, organization):
        """Create departments for private company"""
        departments_data = [
            {'name': 'Information Technology', 'code': 'IT'},
            {'name': 'Human Resources', 'code': 'HR'},
            {'name': 'Finance', 'code': 'FIN'},
            {'name': 'Marketing', 'code': 'MKT'},
            {'name': 'Operations', 'code': 'OPS'},
            {'name': 'Customer Service', 'code': 'CS'},
        ]
        self.create_departments(organization, departments_data)

    def create_government_departments(self, organization):
        """Create departments for government ministry"""
        departments_data = [
            {'name': 'Policy and Planning', 'code': 'PP'},
            {'name': 'Public Health', 'code': 'PH'},
            {'name': 'Medical Services', 'code': 'MS'},
            {'name': 'Health Promotion', 'code': 'HP'},
            {'name': 'Human Resources', 'code': 'HR'},
            {'name': 'Finance and Administration', 'code': 'FA'},
        ]
        self.create_departments(organization, departments_data)

    def create_kra_departments(self, organization):
        """Create departments for KRA"""
        departments_data = [
            {'name': 'Domestic Taxes', 'code': 'DT'},
            {'name': 'Customs and Border Control', 'code': 'CBC'},
            {'name': 'Investigation and Enforcement', 'code': 'IE'},
            {'name': 'Corporate Support Services', 'code': 'CSS'},
            {'name': 'Strategy and Performance', 'code': 'SP'},
            {'name': 'Human Resources', 'code': 'HR'},
        ]
        self.create_departments(organization, departments_data)

    def create_departments(self, organization, departments_data):
        """Create departments for an organization"""
        for dept_data in departments_data:
            dept, created = Department.objects.get_or_create(
                organization=organization,
                name=dept_data['name'],
                defaults={
                    'code': dept_data['code'],
                    'description': f'{dept_data["name"]} department for {organization.name}'
                }
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created department: {dept.name} for {organization.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Sample organization and departments setup completed for {organization.name}!')
        )
