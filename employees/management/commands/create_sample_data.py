"""
Management command to create sample employee data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from employees.models import Department, JobTitle, Employee, SalaryStructure
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Create sample employee data for testing the payroll system'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create departments
        self.create_departments()
        
        # Create job titles
        self.create_job_titles()
        
        # Create employees
        self.create_employees()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )

    def create_departments(self):
        """Create sample departments"""
        self.stdout.write('Creating departments...')
        
        departments = [
            {'name': 'Human Resources', 'code': 'HR', 'description': 'Human Resources Department'},
            {'name': 'Information Technology', 'code': 'IT', 'description': 'IT Department'},
            {'name': 'Finance', 'code': 'FIN', 'description': 'Finance Department'},
            {'name': 'Marketing', 'code': 'MKT', 'description': 'Marketing Department'},
            {'name': 'Operations', 'code': 'OPS', 'description': 'Operations Department'},
            {'name': 'Sales', 'code': 'SAL', 'description': 'Sales Department'},
        ]
        
        for dept_data in departments:
            dept, created = Department.objects.get_or_create(
                code=dept_data['code'],
                defaults={
                    'name': dept_data['name'],
                    'description': dept_data['description']
                }
            )
            if created:
                self.stdout.write(f'  Created department: {dept.name}')

    def create_job_titles(self):
        """Create sample job titles"""
        self.stdout.write('Creating job titles...')
        
        job_titles = [
            'Chief Executive Officer',
            'Chief Technology Officer',
            'Chief Financial Officer',
            'Human Resources Manager',
            'IT Manager',
            'Finance Manager',
            'Marketing Manager',
            'Operations Manager',
            'Sales Manager',
            'Senior Software Developer',
            'Software Developer',
            'Junior Software Developer',
            'Senior Accountant',
            'Accountant',
            'Junior Accountant',
            'Marketing Specialist',
            'Sales Representative',
            'Operations Coordinator',
            'HR Specialist',
            'Administrative Assistant',
        ]
        
        for title in job_titles:
            job_title, created = JobTitle.objects.get_or_create(
                title=title,
                defaults={'description': f'{title} position'}
            )
            if created:
                self.stdout.write(f'  Created job title: {job_title.title}')

    def create_employees(self):
        """Create sample employees with salary structures"""
        self.stdout.write('Creating employees...')
        
        departments = list(Department.objects.all())
        job_titles = list(JobTitle.objects.all())
        
        sample_employees = [
            {
                'first_name': 'John', 'last_name': 'Kamau', 'email': 'john.kamau@company.com',
                'kra_pin': 'A123456789B', 'phone': '+254712345678', 'salary': 250000,
                'department': 'IT', 'job_title': 'Chief Technology Officer'
            },
            {
                'first_name': 'Mary', 'last_name': 'Wanjiku', 'email': 'mary.wanjiku@company.com',
                'kra_pin': 'B987654321C', 'phone': '+254723456789', 'salary': 180000,
                'department': 'HR', 'job_title': 'Human Resources Manager'
            },
            {
                'first_name': 'Peter', 'last_name': 'Ochieng', 'email': 'peter.ochieng@company.com',
                'kra_pin': 'C456789123D', 'phone': '+254734567890', 'salary': 120000,
                'department': 'FIN', 'job_title': 'Finance Manager'
            },
            {
                'first_name': 'Grace', 'last_name': 'Akinyi', 'email': 'grace.akinyi@company.com',
                'kra_pin': 'D789123456E', 'phone': '+254745678901', 'salary': 95000,
                'department': 'IT', 'job_title': 'Senior Software Developer'
            },
            {
                'first_name': 'David', 'last_name': 'Mwangi', 'email': 'david.mwangi@company.com',
                'kra_pin': 'E321654987F', 'phone': '+254756789012', 'salary': 75000,
                'department': 'IT', 'job_title': 'Software Developer'
            },
            {
                'first_name': 'Sarah', 'last_name': 'Njeri', 'email': 'sarah.njeri@company.com',
                'kra_pin': 'F654987321G', 'phone': '+254767890123', 'salary': 85000,
                'department': 'MKT', 'job_title': 'Marketing Manager'
            },
            {
                'first_name': 'James', 'last_name': 'Kiprotich', 'email': 'james.kiprotich@company.com',
                'kra_pin': 'G987321654H', 'phone': '+254778901234', 'salary': 65000,
                'department': 'SAL', 'job_title': 'Sales Manager'
            },
            {
                'first_name': 'Lucy', 'last_name': 'Wambui', 'email': 'lucy.wambui@company.com',
                'kra_pin': 'H123987654I', 'phone': '+254789012345', 'salary': 55000,
                'department': 'FIN', 'job_title': 'Senior Accountant'
            },
            {
                'first_name': 'Michael', 'last_name': 'Otieno', 'email': 'michael.otieno@company.com',
                'kra_pin': 'I456123789J', 'phone': '+254790123456', 'salary': 45000,
                'department': 'IT', 'job_title': 'Junior Software Developer'
            },
            {
                'first_name': 'Anne', 'last_name': 'Chebet', 'email': 'anne.chebet@company.com',
                'kra_pin': 'J789456123K', 'phone': '+254701234567', 'salary': 40000,
                'department': 'HR', 'job_title': 'HR Specialist'
            },
        ]
        
        for emp_data in sample_employees:
            # Get department and job title
            department = Department.objects.get(code=emp_data['department'])
            job_title = JobTitle.objects.get(title=emp_data['job_title'])
            
            # Create employee
            employee, created = Employee.objects.get_or_create(
                email=emp_data['email'],
                defaults={
                    'employee_number': f'EMP{random.randint(1000, 9999)}',
                    'first_name': emp_data['first_name'],
                    'last_name': emp_data['last_name'],
                    'date_of_birth': date.today() - timedelta(days=random.randint(8000, 15000)),
                    'gender': random.choice(['M', 'F']),
                    'marital_status': random.choice(['SINGLE', 'MARRIED']),
                    'phone_number': emp_data['phone'],
                    'address': f'{random.randint(1, 999)} {random.choice(["Kenyatta", "Uhuru", "Moi", "Kibaki"])} Avenue, Nairobi',
                    'department': department,
                    'job_title': job_title,
                    'employment_type': 'PERMANENT',
                    'date_hired': date.today() - timedelta(days=random.randint(30, 1000)),
                    'kra_pin': emp_data['kra_pin'],
                    'nssf_number': f'NSSF{random.randint(100000, 999999)}',
                    'nhif_number': f'NHIF{random.randint(100000, 999999)}',
                    'bank_name': random.choice(['KCB Bank', 'Equity Bank', 'Cooperative Bank', 'Standard Chartered']),
                    'bank_branch': random.choice(['Nairobi', 'Westlands', 'Mombasa', 'Kisumu']),
                    'account_number': f'{random.randint(1000000000, 9999999999)}',
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(f'  Created employee: {employee.full_name}')
                
                # Create salary structure
                basic_salary = Decimal(str(emp_data['salary'] * 0.6))  # 60% basic
                house_allowance = Decimal(str(emp_data['salary'] * 0.25))  # 25% house
                transport_allowance = Decimal(str(emp_data['salary'] * 0.10))  # 10% transport
                other_allowances = Decimal(str(emp_data['salary'] * 0.05))  # 5% other
                
                salary_structure, created = SalaryStructure.objects.get_or_create(
                    employee=employee,
                    defaults={
                        'basic_salary': basic_salary,
                        'house_allowance': house_allowance,
                        'transport_allowance': transport_allowance,
                        'medical_allowance': Decimal('5000'),
                        'lunch_allowance': Decimal('3000'),
                        'communication_allowance': Decimal('2000'),
                        'other_allowances': other_allowances,
                        'life_insurance_premium': Decimal('2000'),
                        'health_insurance_premium': Decimal('3000'),
                        'effective_date': employee.date_hired,
                        'is_active': True
                    }
                )
                
                if created:
                    self.stdout.write(f'    Created salary structure: KES {salary_structure.gross_salary:,}')
