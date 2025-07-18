#!/usr/bin/env python3
"""
Script to create a sample Excel file with 100 employee entries for testing bulk import.
"""

import pandas as pd
import random
from datetime import datetime, timedelta

# Sample data for generating realistic entries
first_names = [
    'John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'James', 'Jessica', 'Robert', 'Ashley',
    'William', 'Amanda', 'Richard', 'Stephanie', 'Joseph', 'Melissa', 'Thomas', 'Nicole', 'Christopher', 'Elizabeth',
    'Daniel', 'Helen', 'Matthew', 'Deborah', 'Anthony', 'Rachel', 'Mark', 'Carolyn', 'Donald', 'Janet',
    'Steven', 'Catherine', 'Paul', 'Maria', 'Andrew', 'Heather', 'Joshua', 'Diane', 'Kenneth', 'Ruth',
    'Kevin', 'Julie', 'Brian', 'Joyce', 'George', 'Virginia', 'Timothy', 'Victoria', 'Ronald', 'Kelly',
    'Ahmed', 'Fatuma', 'Mohamed', 'Amina', 'Hassan', 'Zeinab', 'Ibrahim', 'Halima', 'Omar', 'Mariam',
    'Ali', 'Khadija', 'Yusuf', 'Aisha', 'Abdi', 'Safiya', 'Adan', 'Rahma', 'Farah', 'Nasra',
    'Abdullahi', 'Hawa', 'Issa', 'Sahra', 'Salim', 'Ifrah', 'Hamza', 'Dahabo', 'Khalid', 'Shamsa'
]

middle_names = [
    'James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Charles', 'Joseph', 'Thomas',
    'Mary', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth', 'Barbara', 'Susan', 'Jessica', 'Sarah', 'Karen',
    'Ahmed', 'Mohamed', 'Hassan', 'Ibrahim', 'Omar', 'Ali', 'Yusuf', 'Abdi', 'Adan', 'Farah',
    'Fatuma', 'Amina', 'Zeinab', 'Halima', 'Mariam', 'Khadija', 'Aisha', 'Safiya', 'Rahma', 'Nasra'
]

last_names = [
    'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
    'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin',
    'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson',
    'Walker', 'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores',
    'Hassan', 'Mohamed', 'Ahmed', 'Ali', 'Ibrahim', 'Omar', 'Yusuf', 'Abdi', 'Adan', 'Farah',
    'Abdullahi', 'Issa', 'Salim', 'Hamza', 'Khalid', 'Osman', 'Noor', 'Sheikh', 'Gedi', 'Bare'
]

departments = [
    'Human Resources', 'Finance Department', 'IT Department', 'Marketing Department', 'Operations Department',
    'Sales Department', 'Customer Service', 'Administration', 'Security Department', 'Maintenance Department',
    'Ugatuzi Na Kazi', 'Procurement Department', 'Legal Department', 'Research & Development'
]

job_titles = [
    'Manager', 'Assistant Manager', 'Supervisor', 'Officer', 'Assistant Officer', 'Clerk', 'Secretary',
    'Accountant', 'Cashier', 'Receptionist', 'Security Guard', 'Driver', 'Cleaner', 'Technician',
    'Analyst', 'Coordinator', 'Specialist', 'Executive', 'Administrator', 'Casual Worker'
]

employment_types = ['PERMANENT', 'CONTRACT', 'CASUAL', 'INTERN']

banks = [
    ('01169', 'KCB Bank'),
    ('68058', 'Equity Bank'),
    ('11081', 'Cooperative Bank'),
    ('03017', 'Absa Bank'),
    ('12053', 'National Bank'),
    ('74004', 'Premier Bank'),
    ('72006', 'Gulf African Bank')
]

bank_branches = [
    'Nairobi Branch', 'Mombasa Branch', 'Kisumu Branch', 'Nakuru Branch', 'Eldoret Branch',
    'Thika Branch', 'Machakos Branch', 'Nyeri Branch', 'Meru Branch', 'Garissa Branch'
]

def generate_phone():
    """Generate a Kenyan phone number"""
    prefixes = ['0701', '0702', '0703', '0704', '0705', '0706', '0707', '0708', '0709',
                '0710', '0711', '0712', '0713', '0714', '0715', '0716', '0717', '0718', '0719',
                '0720', '0721', '0722', '0723', '0724', '0725', '0726', '0727', '0728', '0729']
    return f"{random.choice(prefixes)}{random.randint(100000, 999999)}"

def generate_email(first_name, last_name):
    """Generate an email address"""
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'company.co.ke']
    return f"{first_name.lower()}.{last_name.lower()}@{random.choice(domains)}"

def generate_date(start_year=2020, end_year=2024):
    """Generate a random date"""
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    time_between = end_date - start_date
    days_between = time_between.days
    random_days = random.randrange(days_between)
    return (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')

def generate_salary():
    """Generate a salary with various formats"""
    base_salaries = [25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 65000, 70000, 75000, 80000]
    salary = random.choice(base_salaries)
    
    # Return in different formats to test parsing
    formats = [
        str(salary),                    # 50000
        f'"{salary}"',                  # "50000"
        f'"{salary:,}"',               # "50,000"
        f'{salary:,}',                 # 50,000
        f'"{salary}.00"',              # "50000.00"
        f'{salary}.00',                # 50000.00
    ]
    return random.choice(formats)

def generate_id_number():
    """Generate a national ID number"""
    return str(random.randint(10000000, 99999999))

def generate_account_number():
    """Generate a bank account number in various formats"""
    account = random.randint(1000000000, 9999999999)
    
    # Return in different formats
    formats = [
        str(account),
        f'"{account}"',
        f'"{account:,}"',
        f'{account:,}',
    ]
    return random.choice(formats)

# Generate 100 employee records
employees = []

for i in range(100):
    first_name = random.choice(first_names)
    middle_name = random.choice(middle_names) if random.random() > 0.3 else ''  # 70% chance of having middle name
    last_name = random.choice(last_names)
    
    employee = {
        'first_name': first_name,
        'middle_name': middle_name,
        'last_name': last_name,
        'id_number': generate_id_number(),
        'email': generate_email(first_name, last_name) if random.random() > 0.2 else '',  # 80% have email
        'phone': generate_phone(),
        'hire_date': generate_date(),
        'basic_salary': generate_salary(),
        'department_name': random.choice(departments),
        'position_title': random.choice(job_titles),
        'employment_type': random.choice(employment_types),
        'kra_pin': f'A{random.randint(100000000, 999999999)}Z' if random.random() > 0.4 else '',  # 60% have KRA PIN
        'nssf_number': str(random.randint(1000000000, 9999999999)) if random.random() > 0.3 else '',  # 70% have NSSF
        'nhif_number': f'NHIF{random.randint(100000, 999999)}' if random.random() > 0.3 else '',  # 70% have NHIF
    }

    # Handle bank information consistently
    if random.random() > 0.2:  # 80% have bank info
        selected_bank = random.choice(banks)
        employee['bank_code'] = selected_bank[0]
        employee['bank_name'] = selected_bank[1]
        employee['bank_branch'] = random.choice(bank_branches)
    else:
        employee['bank_code'] = ''
        employee['bank_name'] = ''
        employee['bank_branch'] = ''

    # Add account number if bank info exists
    if employee['bank_code']:
        employee['account_number'] = generate_account_number()
    else:
        employee['account_number'] = ''

    employees.append(employee)

# Create DataFrame
df = pd.DataFrame(employees)

# Save to Excel file
output_file = 'sample_employees_100.xlsx'
df.to_excel(output_file, index=False, engine='openpyxl')

print(f"✅ Created {output_file} with {len(employees)} employee records")
print(f"📊 Columns: {list(df.columns)}")
print(f"📁 File saved in current directory")

# Display first few rows as preview
print("\n📋 Preview of first 5 records:")
print(df.head().to_string(index=False))
