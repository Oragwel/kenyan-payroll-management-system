from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.db.models import Sum
from django.template.loader import get_template
from django.utils import timezone
import io
# import xlsxwriter  # Temporarily disabled for deployment
# from reportlab.lib.pagesizes import letter, A4, landscape  # Temporarily disabled for deployment
# from reportlab.lib import colors  # Temporarily disabled for deployment
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle  # Temporarily disabled for deployment
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image  # Temporarily disabled for deployment
# from reportlab.lib.units import inch  # Temporarily disabled for deployment
import os
from employees.models import Employee, Department, JobTitle
from .models import PayrollPeriod, Payslip, PayrollSummary
from statutory_deductions.utils import (
    PAYECalculator, NSSFCalculator, SHIFCalculator,
    AffordableHousingLevyCalculator, validate_statutory_deductions_compliance
)
import json
from decimal import Decimal


@login_required
def dashboard(request):
    """Dashboard view with system statistics - Login required"""
    # Get the active organization
    from employees.models import Organization
    organization = Organization.objects.filter(is_active=True).first()

    context = {
        'total_employees': Employee.objects.count(),
        'active_employees': Employee.objects.filter(is_active=True).count(),
        'total_departments': Department.objects.count(),
        'total_job_titles': JobTitle.objects.count(),
        'organization': organization,
    }
    return render(request, 'dashboard.html', context)


@login_required
def payroll_calculator(request):
    """Payroll calculator view - Login required"""
    # Get organization data
    from employees.models import Organization
    organization = Organization.objects.filter(is_active=True).first()

    context = {
        'organization': organization,
    }
    return render(request, 'payroll/calculator.html', context)


@login_required
def tax_calculator(request):
    """Tax calculator view - Login required"""
    # Get organization data
    from employees.models import Organization
    organization = Organization.objects.filter(is_active=True).first()

    context = {
        'organization': organization,
    }
    return render(request, 'payroll/tax_calculator.html', context)


@csrf_exempt
@login_required
def calculate_payroll_ajax(request):
    """AJAX endpoint for payroll calculations - Login required"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        # Handle both JSON and form data
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            gross_salary = Decimal(str(data.get('gross_salary', 0)))
            employment_type = data.get('employment_type', 'PERMANENT')
        else:
            # Form data
            gross_salary = Decimal(str(request.POST.get('gross_salary', 0)))
            employment_type = request.POST.get('employment_type', 'PERMANENT')

        if gross_salary <= 0:
            return JsonResponse({'error': 'Gross salary must be greater than 0'}, status=400)

        # Initialize calculators
        nssf_calc = NSSFCalculator()
        shif_calc = SHIFCalculator()
        housing_calc = AffordableHousingLevyCalculator()
        paye_calc = PAYECalculator()

        # Calculate NSSF (exempt for contract employees)
        nssf_result = nssf_calc.calculate_nssf_contribution(gross_salary, employment_type)

        # Calculate SHIF (applies to all employment types)
        shif_result = shif_calc.calculate_shif_contribution(gross_salary)

        # Calculate Housing Levy (exempt for contract employees)
        housing_result = housing_calc.calculate_housing_levy(gross_salary, employment_type)

        # Calculate PAYE (after NSSF deduction)
        taxable_income = gross_salary - nssf_result['employee_contribution']

        # Get optional deductions for tax relief
        if request.content_type == 'application/json':
            insurance_premiums = data.get('insurance_premiums')
            mortgage_interest = data.get('mortgage_interest')
            pension_contribution = data.get('pension_contribution')
            post_retirement_medical = data.get('post_retirement_medical')
        else:
            insurance_premiums = request.POST.get('insurance_premiums')
            mortgage_interest = request.POST.get('mortgage_interest')
            pension_contribution = request.POST.get('pension_contribution')
            post_retirement_medical = request.POST.get('post_retirement_medical')

        paye_result = paye_calc.calculate_paye(
            taxable_income=taxable_income,
            insurance_premiums=insurance_premiums,
            mortgage_interest=mortgage_interest,
            pension_contribution=pension_contribution,
            post_retirement_medical=post_retirement_medical
        )

        # Calculate totals
        total_statutory_deductions = (
            nssf_result['employee_contribution'] +
            shif_result['shif_contribution'] +
            housing_result['employee_contribution'] +
            paye_result['paye_tax']
        )

        net_pay = gross_salary - total_statutory_deductions

        # Prepare response
        response_data = {
            'gross_salary': float(gross_salary),
            'employment_type': employment_type,
            'nssf': {
                'employee': float(nssf_result['employee_contribution']),
                'employer': float(nssf_result['employer_contribution']),
                'total': float(nssf_result['total_contribution']),
                'tier_1': float(nssf_result['tier_1_contribution']),
                'tier_2': float(nssf_result['tier_2_contribution']),
                'exemption_reason': nssf_result.get('exemption_reason', ''),
                'applicable': nssf_result.get('applicable', True)
            },
            'shif': {
                'contribution': float(shif_result['shif_contribution']),
                'rate': float(shif_result['contribution_rate']),
                'minimum': float(shif_result['minimum_contribution'])
            },
            'housing_levy': {
                'employee': float(housing_result['employee_contribution']),
                'employer': float(housing_result['employer_contribution']),
                'total': float(housing_result['total_contribution']),
                'exemption_reason': housing_result.get('exemption_reason', ''),
                'applicable': housing_result.get('applicable', True)
            },
            'paye': {
                'taxable_income': float(paye_result['taxable_income']),
                'income_after_deductions': float(paye_result['income_after_deductions']),
                'tax_before_relief': float(paye_result['tax_before_relief']),
                'tax': float(paye_result['paye_tax']),
                'effective_rate': float(paye_result['effective_tax_rate']),
                'reliefs': {
                    'personal': float(paye_result['tax_reliefs']['personal_relief']),
                    'insurance': float(paye_result['tax_reliefs']['insurance_relief']),
                    'total': float(paye_result['tax_reliefs']['total'])
                },
                'deductions': {
                    'mortgage_interest': float(paye_result['allowable_deductions']['mortgage_interest']),
                    'pension_contribution': float(paye_result['allowable_deductions']['pension_contribution']),
                    'post_retirement_medical': float(paye_result['allowable_deductions']['post_retirement_medical']),
                    'total': float(paye_result['allowable_deductions']['total'])
                }
            },
            'totals': {
                'statutory_deductions': float(total_statutory_deductions),
                'net_pay': float(net_pay),
                'take_home_percentage': float((net_pay / gross_salary) * 100) if gross_salary > 0 else 0
            }
        }

        return JsonResponse(response_data)

    except (ValueError, TypeError, KeyError) as e:
        return JsonResponse({'error': f'Invalid input: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Calculation error: {str(e)}'}, status=500)


@login_required
def employee_payroll_detail(request, employee_id):
    """View employee payroll details - Login required"""
    try:
        employee = Employee.objects.get(id=employee_id)
        salary_structure = getattr(employee, 'salary_structure', None)

        if not salary_structure:
            context = {
                'employee': employee,
                'error': 'No salary structure found for this employee'
            }
            return render(request, 'payroll/employee_detail.html', context)

        # Calculate payroll for this employee
        gross_salary = salary_structure.gross_salary

        # Initialize calculators
        nssf_calc = NSSFCalculator()
        shif_calc = SHIFCalculator()
        housing_calc = AffordableHousingLevyCalculator()
        paye_calc = PAYECalculator()

        # Calculate all deductions (pass employment type for contract exemptions)
        nssf_result = nssf_calc.calculate_nssf_contribution(gross_salary, employee.employment_type)
        shif_result = shif_calc.calculate_shif_contribution(gross_salary)
        housing_result = housing_calc.calculate_housing_levy(gross_salary, employee.employment_type)

        # Calculate PAYE with employee's specific deductions
        taxable_income = gross_salary - nssf_result['employee_contribution']
        paye_result = paye_calc.calculate_paye(
            taxable_income=taxable_income,
            insurance_premiums=salary_structure.life_insurance_premium +
                             salary_structure.health_insurance_premium +
                             salary_structure.education_insurance_premium,
            mortgage_interest=salary_structure.mortgage_interest,
            pension_contribution=salary_structure.pension_contribution,
            post_retirement_medical=salary_structure.post_retirement_medical_fund
        )

        # Calculate totals
        total_deductions = (
            nssf_result['employee_contribution'] +
            shif_result['shif_contribution'] +
            housing_result['employee_contribution'] +
            paye_result['paye_tax']
        )

        net_pay = gross_salary - total_deductions

        context = {
            'employee': employee,
            'salary_structure': salary_structure,
            'calculations': {
                'gross_salary': gross_salary,
                'nssf': nssf_result,
                'shif': shif_result,
                'housing_levy': housing_result,
                'paye': paye_result,
                'total_deductions': total_deductions,
                'net_pay': net_pay
            }
        }

        return render(request, 'payroll/employee_detail.html', context)

    except Employee.DoesNotExist:
        return render(request, 'payroll/employee_detail.html', {
            'error': 'Employee not found'
        })
    except Exception as e:
        return render(request, 'payroll/employee_detail.html', {
            'error': f'Error calculating payroll: {str(e)}'
        })


@staff_member_required
def generate_payslip(request, employee_id):
    """Generate a payslip for an employee - Admin only"""
    try:
        employee = Employee.objects.get(id=employee_id)
        salary_structure = getattr(employee, 'salary_structure', None)

        if not salary_structure:
            return render(request, 'payroll/payslip.html', {
                'error': 'No salary structure found for this employee',
                'employee': employee
            })

        # Create a mock payroll period for demonstration
        from datetime import date, timedelta
        from .models import PayrollPeriod, Payslip

        # Try to get or create a current month payroll period
        today = date.today()
        start_date = today.replace(day=1)
        if today.month == 12:
            end_date = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end_date = today.replace(month=today.month + 1, day=1) - timedelta(days=1)

        payroll_period, created = PayrollPeriod.objects.get_or_create(
            start_date=start_date,
            end_date=end_date,
            defaults={
                'name': f"{start_date.strftime('%B %Y')} Payroll",
                'period_type': 'MONTHLY',
                'pay_date': end_date + timedelta(days=3),
                'status': 'DRAFT',
                'created_by_id': 1  # Default admin user
            }
        )

        # Calculate payroll for this employee
        gross_salary = salary_structure.gross_salary

        # Initialize calculators
        nssf_calc = NSSFCalculator()
        shif_calc = SHIFCalculator()
        housing_calc = AffordableHousingLevyCalculator()
        paye_calc = PAYECalculator()

        # Calculate all deductions (pass employment type for contract exemptions)
        nssf_result = nssf_calc.calculate_nssf_contribution(gross_salary, employee.employment_type)
        shif_result = shif_calc.calculate_shif_contribution(gross_salary)
        housing_result = housing_calc.calculate_housing_levy(gross_salary, employee.employment_type)

        # Calculate PAYE with employee's specific deductions
        taxable_income = gross_salary - nssf_result['employee_contribution']
        paye_result = paye_calc.calculate_paye(
            taxable_income=taxable_income,
            insurance_premiums=salary_structure.life_insurance_premium +
                             salary_structure.health_insurance_premium +
                             salary_structure.education_insurance_premium,
            mortgage_interest=salary_structure.mortgage_interest,
            pension_contribution=salary_structure.pension_contribution,
            post_retirement_medical=salary_structure.post_retirement_medical_fund
        )

        # Calculate totals
        total_deductions = (
            nssf_result['employee_contribution'] +
            shif_result['shif_contribution'] +
            housing_result['employee_contribution'] +
            paye_result['paye_tax']
        )

        net_pay = gross_salary - total_deductions

        # Create or update payslip
        payslip, created = Payslip.objects.get_or_create(
            payroll_period=payroll_period,
            employee=employee,
            defaults={
                'basic_salary': salary_structure.basic_salary,
                'house_allowance': salary_structure.house_allowance,
                'transport_allowance': salary_structure.transport_allowance,
                'medical_allowance': salary_structure.medical_allowance,
                'lunch_allowance': salary_structure.lunch_allowance,
                'communication_allowance': salary_structure.communication_allowance,
                'other_allowances': salary_structure.other_allowances,
                'car_benefit': salary_structure.car_benefit_value,
                'housing_benefit': salary_structure.housing_benefit_value,
                'gross_pay': gross_salary,
                'paye_tax': paye_result['paye_tax'],
                'nssf_employee': nssf_result['employee_contribution'],
                'nssf_employer': nssf_result['employer_contribution'],
                'shif_contribution': shif_result['shif_contribution'],
                'housing_levy_employee': housing_result['employee_contribution'],
                'housing_levy_employer': housing_result['employer_contribution'],
                'total_deductions': total_deductions,
                'net_pay': net_pay,
                'personal_relief': paye_result['tax_reliefs']['personal_relief'],
                'insurance_relief': paye_result['tax_reliefs']['insurance_relief'],
            }
        )

        # Get organization data
        from employees.models import Organization
        organization = Organization.objects.filter(is_active=True).first()

        context = {
            'employee': employee,
            'salary_structure': salary_structure,
            'payroll_period': payroll_period,
            'payslip': payslip,
            'organization': organization,
        }

        return render(request, 'payroll/payslip.html', context)

    except Employee.DoesNotExist:
        return render(request, 'payroll/payslip.html', {
            'error': 'Employee not found'
        })
    except Exception as e:
        return render(request, 'payroll/payslip.html', {
            'error': f'Error generating payslip: {str(e)}'
        })


@login_required
def view_payslip(request, payslip_id):
    """View an existing payslip by payslip ID"""
    try:
        payslip = Payslip.objects.select_related('employee', 'payroll_period').get(id=payslip_id)

        # Get organization data
        from employees.models import Organization
        organization = Organization.objects.filter(is_active=True).first()

        context = {
            'employee': payslip.employee,
            'payroll_period': payslip.payroll_period,
            'payslip': payslip,
            'organization': organization,
        }

        return render(request, 'payroll/payslip.html', context)

    except Payslip.DoesNotExist:
        return render(request, 'payroll/payslip.html', {
            'error': 'Payslip not found'
        })
    except Exception as e:
        return render(request, 'payroll/payslip.html', {
            'error': f'Error viewing payslip: {str(e)}'
        })


@login_required
def payroll_reports(request):
    """Generate comprehensive payroll reports - Login required"""
    # Get the active organization
    from employees.models import Organization
    organization = Organization.objects.filter(is_active=True).first()

    # Get all active employees with salary structures
    employees_with_salary = Employee.objects.filter(
        is_active=True,
        salary_structure__is_active=True
    ).select_related('salary_structure', 'department')

    if not employees_with_salary.exists():
        context = {
            'total_employees': 0,
            'total_gross_payroll': 0,
            'total_net_payroll': 0,
            'average_tax_rate': 0,
            'department_analysis': [],
            'salary_ranges': [],
            'total_paye': 0,
            'total_nssf_employee': 0,
            'total_shif': 0,
            'total_housing_levy': 0,
            'total_tax_relief': 0,
            'employees_with_relief': 0,
            'organization': organization,
        }
        return render(request, 'payroll/reports.html', context)

    # Initialize calculators
    nssf_calc = NSSFCalculator()
    shif_calc = SHIFCalculator()
    housing_calc = AffordableHousingLevyCalculator()
    paye_calc = PAYECalculator()

    # Calculate totals
    total_employees = employees_with_salary.count()
    total_gross_payroll = 0
    total_net_payroll = 0
    total_paye = 0
    total_nssf_employee = 0
    total_shif = 0
    total_housing_levy = 0
    total_tax_relief = 0
    employees_with_relief = 0

    # Department analysis
    department_data = {}

    # Salary range analysis
    salary_ranges = {
        'Under 30K': 0,
        '30K - 50K': 0,
        '50K - 100K': 0,
        '100K - 200K': 0,
        'Over 200K': 0
    }

    for employee in employees_with_salary:
        salary_structure = employee.salary_structure
        gross_salary = salary_structure.gross_salary

        # Calculate deductions for this employee (pass employment type for contract exemptions)
        nssf_result = nssf_calc.calculate_nssf_contribution(gross_salary, employee.employment_type)
        shif_result = shif_calc.calculate_shif_contribution(gross_salary)
        housing_result = housing_calc.calculate_housing_levy(gross_salary, employee.employment_type)

        # Calculate PAYE
        taxable_income = gross_salary - nssf_result['employee_contribution']
        paye_result = paye_calc.calculate_paye(
            taxable_income=taxable_income,
            insurance_premiums=salary_structure.life_insurance_premium +
                             salary_structure.health_insurance_premium +
                             salary_structure.education_insurance_premium,
            mortgage_interest=salary_structure.mortgage_interest,
            pension_contribution=salary_structure.pension_contribution,
            post_retirement_medical=salary_structure.post_retirement_medical_fund
        )

        # Calculate net pay
        total_deductions = (
            nssf_result['employee_contribution'] +
            shif_result['shif_contribution'] +
            housing_result['employee_contribution'] +
            paye_result['paye_tax']
        )
        net_pay = gross_salary - total_deductions

        # Add to totals
        total_gross_payroll += gross_salary
        total_net_payroll += net_pay
        total_paye += paye_result['paye_tax']
        total_nssf_employee += nssf_result['employee_contribution']
        total_shif += shif_result['shif_contribution']
        total_housing_levy += housing_result['employee_contribution']
        total_tax_relief += paye_result['tax_reliefs']['total']

        if paye_result['tax_reliefs']['total'] > paye_result['tax_reliefs']['personal_relief']:
            employees_with_relief += 1

        # Department analysis
        dept_name = employee.department.name
        if dept_name not in department_data:
            department_data[dept_name] = {
                'department__name': dept_name,
                'department__code': employee.department.code,
                'employee_count': 0,
                'total_gross': 0,
                'avg_salary': 0
            }

        department_data[dept_name]['employee_count'] += 1
        department_data[dept_name]['total_gross'] += gross_salary

        # Salary range analysis
        if gross_salary < 30000:
            salary_ranges['Under 30K'] += 1
        elif gross_salary < 50000:
            salary_ranges['30K - 50K'] += 1
        elif gross_salary < 100000:
            salary_ranges['50K - 100K'] += 1
        elif gross_salary < 200000:
            salary_ranges['100K - 200K'] += 1
        else:
            salary_ranges['Over 200K'] += 1

    # Calculate averages for departments
    for dept in department_data.values():
        dept['avg_salary'] = dept['total_gross'] / dept['employee_count'] if dept['employee_count'] > 0 else 0

    # Convert salary ranges to list with percentages
    salary_ranges_list = []
    for range_label, count in salary_ranges.items():
        percentage = (count / total_employees * 100) if total_employees > 0 else 0
        salary_ranges_list.append({
            'range_label': range_label,
            'count': count,
            'percentage': percentage
        })

    # Calculate percentages
    average_tax_rate = (total_paye / total_gross_payroll * 100) if total_gross_payroll > 0 else 0
    paye_percentage = (total_paye / total_gross_payroll * 100) if total_gross_payroll > 0 else 0
    nssf_percentage = (total_nssf_employee / total_gross_payroll * 100) if total_gross_payroll > 0 else 0
    shif_percentage = (total_shif / total_gross_payroll * 100) if total_gross_payroll > 0 else 0
    housing_levy_percentage = (total_housing_levy / total_gross_payroll * 100) if total_gross_payroll > 0 else 0

    # Additional data for charts
    from django.db.models import Count

    # Department statistics for charts
    department_stats = []
    for dept_name, dept_info in department_data.items():
        department_stats.append({
            'department__name': dept_name,
            'total_gross': dept_info['total_gross'],
            'count': dept_info['employee_count']
        })

    # Employment type statistics
    employment_type_stats = employees_with_salary.values('employment_type').annotate(
        count=Count('id')
    )

    # Calculate average deductions for charts
    avg_salary = total_gross_payroll / total_employees if total_employees > 0 else 0
    avg_paye = total_paye / total_employees if total_employees > 0 else 0
    avg_nssf = total_nssf_employee / total_employees if total_employees > 0 else 0
    avg_shif = total_shif / total_employees if total_employees > 0 else 0
    avg_housing_levy = total_housing_levy / total_employees if total_employees > 0 else 0
    avg_other_deductions = 500  # Placeholder for other deductions

    context = {
        'total_employees': total_employees,
        'total_gross_payroll': total_gross_payroll,
        'total_net_payroll': total_net_payroll,
        'average_tax_rate': average_tax_rate,
        'department_analysis': list(department_data.values()),
        'salary_ranges': salary_ranges_list,
        'total_paye': total_paye,
        'total_nssf_employee': total_nssf_employee,
        'total_shif': total_shif,
        'total_housing_levy': total_housing_levy,
        'total_tax_relief': total_tax_relief,
        'employees_with_relief': employees_with_relief,
        'paye_percentage': paye_percentage,
        'nssf_percentage': nssf_percentage,
        'shif_percentage': shif_percentage,
        'housing_levy_percentage': housing_levy_percentage,
        # Chart data
        'department_stats': department_stats,
        'employment_type_stats': employment_type_stats,
        'avg_paye': avg_paye,
        'avg_nssf': avg_nssf,
        'avg_shif': avg_shif,
        'avg_housing_levy': avg_housing_levy,
        'avg_other_deductions': avg_other_deductions,
        'employees': employees_with_salary,  # For JavaScript calculations
        'organization': organization,
    }

    return render(request, 'payroll/reports.html', context)


@login_required
def export_payroll_summary(request):
    """Export payroll summary to Excel"""
    import io
    import xlsxwriter
    from django.http import HttpResponse
    from employees.models import Organization

    # Get organization
    organization = Organization.objects.filter(is_active=True).first()

    # Get employees with salary structures
    employees = Employee.objects.filter(
        is_active=True,
        salary_structure__is_active=True
    ).select_related('salary_structure', 'department')

    # Create Excel file
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet('Payroll Summary')

    # Define formats
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#4472C4',
        'font_color': 'white',
        'border': 1
    })

    title_format = workbook.add_format({
        'bold': True,
        'font_size': 20,
        'align': 'center'
    })

    org_name_format = workbook.add_format({
        'bold': True,
        'font_size': 18,
        'align': 'center'
    })

    org_format = workbook.add_format({
        'font_size': 14,
        'align': 'center'
    })

    money_format = workbook.add_format({'num_format': '#,##0.00'})

    # Add organization header
    current_row = 0
    if organization:
        # Organization name
        worksheet.merge_range(current_row, 0, current_row, 9, organization.name, org_name_format)
        current_row += 1

        # Complete address
        address_parts = []
        if organization.address_line_1:
            address_parts.append(organization.address_line_1)
        if organization.address_line_2:
            address_parts.append(organization.address_line_2)
        if organization.city:
            address_parts.append(organization.city)
        if organization.postal_code:
            address_parts.append(f"P.O. Box {organization.postal_code}")
        if organization.country:
            address_parts.append(organization.country)

        if address_parts:
            full_address = ", ".join(address_parts)
            worksheet.merge_range(current_row, 0, current_row, 9, full_address, org_format)
            current_row += 1

        # Contact information
        contact_info = []
        if organization.phone_number:
            contact_info.append(f"Tel: {organization.phone_number}")
        if organization.email:
            contact_info.append(f"Email: {organization.email}")
        if organization.website:
            contact_info.append(f"Web: {organization.website}")

        if contact_info:
            worksheet.merge_range(current_row, 0, current_row, 9, " | ".join(contact_info), org_format)
            current_row += 1

        # KRA PIN
        if organization.kra_pin:
            worksheet.merge_range(current_row, 0, current_row, 9, f"KRA PIN: {organization.kra_pin}", org_format)
            current_row += 1

        # Report title
        worksheet.merge_range(current_row, 0, current_row, 9, "PAYROLL SUMMARY REPORT", title_format)
        current_row += 2

    # Write headers
    headers = [
        'Employee No', 'Name', 'Department', 'Employment Type',
        'Basic Salary', 'PAYE', 'NSSF', 'SHIF', 'Housing Levy', 'Net Pay'
    ]

    for col, header in enumerate(headers):
        worksheet.write(current_row, col, header, header_format)

    # Initialize calculators
    from statutory_deductions.utils import NSSFCalculator, SHIFCalculator, AffordableHousingLevyCalculator, PAYECalculator
    nssf_calc = NSSFCalculator()
    shif_calc = SHIFCalculator()
    housing_calc = AffordableHousingLevyCalculator()
    paye_calc = PAYECalculator()

    # Write data
    row = current_row + 1
    for employee in employees:
        basic_salary = employee.salary_structure.basic_salary

        # Calculate deductions (pass employment type for contract exemptions)
        nssf_result = nssf_calc.calculate_nssf_contribution(basic_salary, employee.employment_type)
        shif_result = shif_calc.calculate_shif_contribution(basic_salary)
        housing_result = housing_calc.calculate_housing_levy(basic_salary, employee.employment_type)

        nssf = nssf_result['employee_contribution']
        shif = shif_result['shif_contribution']
        housing_levy = housing_result['employee_contribution']

        # Calculate taxable income
        taxable_income = basic_salary - nssf
        paye_result = paye_calc.calculate_paye(taxable_income)
        paye = paye_result['paye_tax']

        # Calculate net pay
        total_deductions = paye + nssf + shif + housing_levy
        net_pay = basic_salary - total_deductions

        # Write row data
        worksheet.write(row, 0, employee.payroll_number or '')
        worksheet.write(row, 1, f"{employee.first_name} {employee.last_name}")
        worksheet.write(row, 2, employee.department.name if employee.department else 'N/A')
        worksheet.write(row, 3, employee.get_employment_type_display())
        worksheet.write(row, 4, basic_salary, money_format)
        worksheet.write(row, 5, paye, money_format)
        worksheet.write(row, 6, nssf, money_format)
        worksheet.write(row, 7, shif, money_format)
        worksheet.write(row, 8, housing_levy, money_format)
        worksheet.write(row, 9, net_pay, money_format)

        row += 1

    # Auto-adjust column widths
    worksheet.set_column('A:A', 12)
    worksheet.set_column('B:B', 25)
    worksheet.set_column('C:C', 20)
    worksheet.set_column('D:D', 15)
    worksheet.set_column('E:J', 12)

    workbook.close()
    output.seek(0)

    # Create response
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    org_name = organization.name if organization else "Organization"
    response['Content-Disposition'] = f'attachment; filename="{org_name}_Payroll_Summary.xlsx"'

    return response


@login_required
def export_tax_report(request):
    """Export tax report to PDF"""
    import io
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.units import inch
    from django.http import HttpResponse
    from employees.models import Organization

    # Get organization
    organization = Organization.objects.filter(is_active=True).first()

    # Get employees with salary structures
    employees = Employee.objects.filter(
        is_active=True,
        salary_structure__is_active=True
    ).select_related('salary_structure', 'department')

    # Create PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), topMargin=0.5*inch)

    # Container for the 'Flowable' objects
    elements = []

    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=20,
        alignment=1  # Center alignment
    )

    org_name_style = ParagraphStyle(
        'OrgNameStyle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=10,
        alignment=1  # Center alignment
    )

    org_style = ParagraphStyle(
        'OrgStyle',
        parent=styles['Normal'],
        fontSize=14,
        spaceAfter=8,
        alignment=1  # Center alignment
    )

    # Add organization header with logo
    if organization:
        # Create header table with logo and organization info
        header_data = []

        # Try to add logo if available
        logo_cell = ""
        if organization.logo:
            try:
                from reportlab.platypus import Image
                logo = Image(organization.logo.path, width=1.5*inch, height=1.5*inch)
                logo_cell = logo
            except:
                logo_cell = ""

        # Organization info with complete details
        address_parts = []
        if organization.address_line_1:
            address_parts.append(organization.address_line_1)
        if organization.address_line_2:
            address_parts.append(organization.address_line_2)
        if organization.city:
            address_parts.append(organization.city)
        if organization.postal_code:
            address_parts.append(f"P.O. Box {organization.postal_code}")
        if organization.country:
            address_parts.append(organization.country)

        full_address = ", ".join(address_parts)

        org_info_parts = [
            Paragraph(f"<b>{organization.name}</b>", org_name_style),
        ]

        if full_address:
            org_info_parts.append(Paragraph(full_address, org_style))

        contact_info = []
        if organization.phone_number:
            contact_info.append(f"Tel: {organization.phone_number}")
        if organization.email:
            contact_info.append(f"Email: {organization.email}")
        if organization.website:
            contact_info.append(f"Web: {organization.website}")

        if contact_info:
            org_info_parts.append(Paragraph(" | ".join(contact_info), org_style))

        if organization.kra_pin:
            org_info_parts.append(Paragraph(f"KRA PIN: {organization.kra_pin}", org_style))

        if logo_cell:
            header_data = [[logo_cell, org_info_parts]]
            header_table = Table(header_data, colWidths=[2*inch, 6*inch])
            header_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ]))
            elements.append(header_table)
        else:
            for part in org_info_parts:
                elements.append(part)

        elements.append(Spacer(1, 20))

    # Add title
    title = Paragraph("PAYE Tax Report", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Prepare table data
    data = [['Employee No', 'Name', 'Department', 'Basic Salary', 'Taxable Income', 'PAYE Tax', 'Tax Rate %']]

    # Initialize calculators
    from statutory_deductions.utils import NSSFCalculator, PAYECalculator
    nssf_calc = NSSFCalculator()
    paye_calc = PAYECalculator()

    total_basic = 0
    total_taxable = 0
    total_paye = 0

    for employee in employees:
        basic_salary = employee.salary_structure.basic_salary
        nssf_result = nssf_calc.calculate_nssf_contribution(basic_salary, employee.employment_type)
        nssf = nssf_result['employee_contribution']
        taxable_income = basic_salary - nssf
        paye_result = paye_calc.calculate_paye(taxable_income)
        paye = paye_result['paye_tax']
        tax_rate = (paye / taxable_income * 100) if taxable_income > 0 else 0

        total_basic += basic_salary
        total_taxable += taxable_income
        total_paye += paye

        data.append([
            employee.payroll_number or '',
            f"{employee.first_name} {employee.last_name}",
            employee.department.name if employee.department else 'N/A',
            f"KES {basic_salary:,.2f}",
            f"KES {taxable_income:,.2f}",
            f"KES {paye:,.2f}",
            f"{tax_rate:.1f}%"
        ])

    # Add totals row
    avg_tax_rate = (total_paye / total_taxable * 100) if total_taxable > 0 else 0
    data.append([
        'TOTAL', '', '',
        f"KES {total_basic:,.2f}",
        f"KES {total_taxable:,.2f}",
        f"KES {total_paye:,.2f}",
        f"{avg_tax_rate:.1f}%"
    ])

    # Create table with larger column widths for landscape orientation
    table = Table(data, colWidths=[1.2*inch, 2.5*inch, 1.8*inch, 1.5*inch, 1.5*inch, 1.5*inch, 1.2*inch])

    # Add style to table with larger fonts and better spacing
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),  # Larger header font
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),  # Larger data font
        ('BOTTOMPADDING', (0, 0), (-1, 0), 15),  # More padding
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 11),  # Larger totals font
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Vertical alignment
    ]))

    elements.append(table)

    # Build PDF
    doc.build(elements)

    # Get the value of the BytesIO buffer and write it to the response
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    org_name = organization.name if organization else "Organization"
    response['Content-Disposition'] = f'attachment; filename="{org_name}_Tax_Report.pdf"'
    response.write(pdf)

    return response


@login_required
def export_statutory_returns(request):
    """Export statutory returns (NSSF, SHIF, Housing Levy) to Excel"""
    import io
    import xlsxwriter
    from django.http import HttpResponse
    from employees.models import Organization

    # Get organization
    organization = Organization.objects.filter(is_active=True).first()

    # Get employees with salary structures
    employees = Employee.objects.filter(
        is_active=True,
        salary_structure__is_active=True
    ).select_related('salary_structure', 'department')

    # Create Excel file
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)

    # Create worksheets for each statutory return
    nssf_sheet = workbook.add_worksheet('NSSF Returns')
    shif_sheet = workbook.add_worksheet('SHIF Returns')
    housing_sheet = workbook.add_worksheet('Housing Levy Returns')

    # Define formats
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#4472C4',
        'font_color': 'white',
        'border': 1
    })

    title_format = workbook.add_format({
        'bold': True,
        'font_size': 20,
        'align': 'center'
    })

    org_name_format = workbook.add_format({
        'bold': True,
        'font_size': 18,
        'align': 'center'
    })

    org_format = workbook.add_format({
        'font_size': 14,
        'align': 'center'
    })

    money_format = workbook.add_format({'num_format': '#,##0.00'})

    # Initialize calculators
    from statutory_deductions.utils import NSSFCalculator, SHIFCalculator, AffordableHousingLevyCalculator
    nssf_calc = NSSFCalculator()
    shif_calc = SHIFCalculator()
    housing_calc = AffordableHousingLevyCalculator()

    # Helper function to add organization header to worksheet
    def add_org_header(sheet, title, max_cols):
        current_row = 0
        if organization:
            # Organization name
            sheet.merge_range(current_row, 0, current_row, max_cols-1, organization.name, org_name_format)
            current_row += 1

            # Complete address
            address_parts = []
            if organization.address_line_1:
                address_parts.append(organization.address_line_1)
            if organization.address_line_2:
                address_parts.append(organization.address_line_2)
            if organization.city:
                address_parts.append(organization.city)
            if organization.postal_code:
                address_parts.append(f"P.O. Box {organization.postal_code}")
            if organization.country:
                address_parts.append(organization.country)

            if address_parts:
                full_address = ", ".join(address_parts)
                sheet.merge_range(current_row, 0, current_row, max_cols-1, full_address, org_format)
                current_row += 1

            # Contact information
            contact_info = []
            if organization.phone_number:
                contact_info.append(f"Tel: {organization.phone_number}")
            if organization.email:
                contact_info.append(f"Email: {organization.email}")
            if organization.website:
                contact_info.append(f"Web: {organization.website}")

            if contact_info:
                sheet.merge_range(current_row, 0, current_row, max_cols-1, " | ".join(contact_info), org_format)
                current_row += 1

            # KRA PIN
            if organization.kra_pin:
                sheet.merge_range(current_row, 0, current_row, max_cols-1, f"KRA PIN: {organization.kra_pin}", org_format)
                current_row += 1

            # Report title
            sheet.merge_range(current_row, 0, current_row, max_cols-1, title, title_format)
            current_row += 2
        return current_row

    # NSSF Returns Sheet
    nssf_headers = ['Employee No', 'Name', 'National ID', 'Basic Salary', 'Employee Contribution', 'Employer Contribution', 'Total Contribution']
    nssf_header_row = add_org_header(nssf_sheet, "NSSF RETURNS", len(nssf_headers))
    for col, header in enumerate(nssf_headers):
        nssf_sheet.write(nssf_header_row, col, header, header_format)

    # SHIF Returns Sheet
    shif_headers = ['Employee No', 'Name', 'SHIF Number', 'Basic Salary', 'SHIF Contribution']
    shif_header_row = add_org_header(shif_sheet, "SHIF RETURNS", len(shif_headers))
    for col, header in enumerate(shif_headers):
        shif_sheet.write(shif_header_row, col, header, header_format)

    # Housing Levy Returns Sheet
    housing_headers = ['Employee No', 'Name', 'Basic Salary', 'Employee Contribution', 'Employer Contribution', 'Total Contribution']
    housing_header_row = add_org_header(housing_sheet, "HOUSING LEVY RETURNS", len(housing_headers))
    for col, header in enumerate(housing_headers):
        housing_sheet.write(housing_header_row, col, header, header_format)

    # Write data
    row = max(nssf_header_row, shif_header_row, housing_header_row) + 1
    total_nssf_employee = 0
    total_nssf_employer = 0
    total_shif = 0
    total_housing_employee = 0
    total_housing_employer = 0

    for employee in employees:
        basic_salary = employee.salary_structure.basic_salary

        # Calculate contributions (pass employment type for contract exemptions)
        nssf_result = nssf_calc.calculate_nssf_contribution(basic_salary, employee.employment_type)
        shif_result = shif_calc.calculate_shif_contribution(basic_salary)
        housing_result = housing_calc.calculate_housing_levy(basic_salary, employee.employment_type)

        nssf_employee = nssf_result['employee_contribution']
        nssf_employer = nssf_result['employer_contribution']
        shif = shif_result['shif_contribution']
        housing_employee = housing_result['employee_contribution']
        housing_employer = housing_result['employer_contribution']

        # Update totals
        total_nssf_employee += nssf_employee
        total_nssf_employer += nssf_employer
        total_shif += shif
        total_housing_employee += housing_employee
        total_housing_employer += housing_employer

        # NSSF Sheet
        nssf_sheet.write(row, 0, employee.payroll_number or '')
        nssf_sheet.write(row, 1, f"{employee.first_name} {employee.last_name}")
        nssf_sheet.write(row, 2, employee.national_id or '')
        nssf_sheet.write(row, 3, basic_salary, money_format)
        nssf_sheet.write(row, 4, nssf_employee, money_format)
        nssf_sheet.write(row, 5, nssf_employer, money_format)
        nssf_sheet.write(row, 6, nssf_employee + nssf_employer, money_format)

        # SHIF Sheet
        shif_sheet.write(row, 0, employee.payroll_number or '')
        shif_sheet.write(row, 1, f"{employee.first_name} {employee.last_name}")
        shif_sheet.write(row, 2, employee.shif_number or '')
        shif_sheet.write(row, 3, basic_salary, money_format)
        shif_sheet.write(row, 4, shif, money_format)

        # Housing Levy Sheet
        housing_sheet.write(row, 0, employee.payroll_number or '')
        housing_sheet.write(row, 1, f"{employee.first_name} {employee.last_name}")
        housing_sheet.write(row, 2, basic_salary, money_format)
        housing_sheet.write(row, 3, housing_employee, money_format)
        housing_sheet.write(row, 4, housing_employer, money_format)
        housing_sheet.write(row, 5, housing_employee + housing_employer, money_format)

        row += 1

    # Add totals rows
    for sheet, totals in [
        (nssf_sheet, ['TOTAL', '', '', '', total_nssf_employee, total_nssf_employer, total_nssf_employee + total_nssf_employer]),
        (shif_sheet, ['TOTAL', '', '', '', total_shif]),
        (housing_sheet, ['TOTAL', '', '', total_housing_employee, total_housing_employer, total_housing_employee + total_housing_employer])
    ]:
        for col, value in enumerate(totals):
            if isinstance(value, (int, float)) and col > 2:
                sheet.write(row, col, value, money_format)
            else:
                sheet.write(row, col, value, header_format)

    # Auto-adjust column widths for all sheets
    for sheet in [nssf_sheet, shif_sheet, housing_sheet]:
        sheet.set_column('A:A', 12)
        sheet.set_column('B:B', 25)
        sheet.set_column('C:G', 15)

    workbook.close()
    output.seek(0)

    # Create response
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    org_name = organization.name if organization else "Organization"
    response['Content-Disposition'] = f'attachment; filename="{org_name}_Statutory_Returns.xlsx"'

    return response


@login_required
def export_employee_list(request):
    """Export employee list to Excel"""
    import io
    import xlsxwriter
    from django.http import HttpResponse
    from employees.models import Organization

    # Get organization
    organization = Organization.objects.filter(is_active=True).first()

    # Get all employees
    employees = Employee.objects.all().select_related('department', 'job_title', 'salary_structure')

    # Create Excel file
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet('Employee List')

    # Define formats
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#4472C4',
        'font_color': 'white',
        'border': 1
    })

    title_format = workbook.add_format({
        'bold': True,
        'font_size': 20,
        'align': 'center'
    })

    org_name_format = workbook.add_format({
        'bold': True,
        'font_size': 18,
        'align': 'center'
    })

    org_format = workbook.add_format({
        'font_size': 14,
        'align': 'center'
    })

    date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})
    money_format = workbook.add_format({'num_format': '#,##0.00'})

    # Add organization header
    current_row = 0
    if organization:
        # Organization name
        worksheet.merge_range(current_row, 0, current_row, 12, organization.name, org_name_format)
        current_row += 1

        # Complete address
        address_parts = []
        if organization.address_line_1:
            address_parts.append(organization.address_line_1)
        if organization.address_line_2:
            address_parts.append(organization.address_line_2)
        if organization.city:
            address_parts.append(organization.city)
        if organization.postal_code:
            address_parts.append(f"P.O. Box {organization.postal_code}")
        if organization.country:
            address_parts.append(organization.country)

        if address_parts:
            full_address = ", ".join(address_parts)
            worksheet.merge_range(current_row, 0, current_row, 12, full_address, org_format)
            current_row += 1

        # Contact information
        contact_info = []
        if organization.phone_number:
            contact_info.append(f"Tel: {organization.phone_number}")
        if organization.email:
            contact_info.append(f"Email: {organization.email}")
        if organization.website:
            contact_info.append(f"Web: {organization.website}")

        if contact_info:
            worksheet.merge_range(current_row, 0, current_row, 12, " | ".join(contact_info), org_format)
            current_row += 1

        # KRA PIN
        if organization.kra_pin:
            worksheet.merge_range(current_row, 0, current_row, 12, f"KRA PIN: {organization.kra_pin}", org_format)
            current_row += 1

        # Report title
        worksheet.merge_range(current_row, 0, current_row, 12, "EMPLOYEE LIST", title_format)
        current_row += 2

    # Write headers
    headers = [
        'Employee No', 'First Name', 'Last Name', 'National ID', 'Email',
        'Department', 'Job Title', 'Employment Type', 'Date Hired',
        'Basic Salary', 'SHIF Number', 'NSSF Number', 'Status'
    ]

    for col, header in enumerate(headers):
        worksheet.write(current_row, col, header, header_format)

    # Write data
    row = current_row + 1
    for employee in employees:
        worksheet.write(row, 0, employee.payroll_number or '')
        worksheet.write(row, 1, employee.first_name)
        worksheet.write(row, 2, employee.last_name)
        worksheet.write(row, 3, employee.national_id or '')
        worksheet.write(row, 4, employee.email or '')
        worksheet.write(row, 5, employee.department.name if employee.department else 'N/A')
        worksheet.write(row, 6, employee.job_title.title if employee.job_title else 'N/A')
        worksheet.write(row, 7, employee.get_employment_type_display())

        if employee.date_hired:
            worksheet.write(row, 8, employee.date_hired, date_format)
        else:
            worksheet.write(row, 8, 'N/A')

        if employee.salary_structure:
            worksheet.write(row, 9, employee.salary_structure.basic_salary, money_format)
        else:
            worksheet.write(row, 9, 'N/A')

        worksheet.write(row, 10, employee.shif_number or '')
        worksheet.write(row, 11, employee.nssf_number or '')
        worksheet.write(row, 12, 'Active' if employee.is_active else 'Inactive')

        row += 1

    # Auto-adjust column widths
    worksheet.set_column('A:A', 12)
    worksheet.set_column('B:C', 15)
    worksheet.set_column('D:D', 15)
    worksheet.set_column('E:E', 25)
    worksheet.set_column('F:G', 20)
    worksheet.set_column('H:H', 15)
    worksheet.set_column('I:I', 12)
    worksheet.set_column('J:J', 12)
    worksheet.set_column('K:L', 15)
    worksheet.set_column('M:M', 10)

    workbook.close()
    output.seek(0)

    # Create response
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    org_name = organization.name if organization else "Organization"
    response['Content-Disposition'] = f'attachment; filename="{org_name}_Employee_List.xlsx"'

    return response


@staff_member_required
def payroll_generation(request):
    """Generate payroll for selected month/year - Admin only"""
    from datetime import date, datetime
    from calendar import monthrange

    today = date.today()

    # Get organization data
    from employees.models import Organization
    organization = Organization.objects.filter(is_active=True).first()

    context = {
        'current_year': today.year,
        'current_month': today.month,
        'today': today,
        'months': [
            (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
            (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
            (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
        ],
        'years': list(range(2020, today.year + 1)),  # 2020 to current year only
        'organization': organization,
    }

    if request.method == 'POST':
        try:
            selected_month = int(request.POST.get('month'))
            selected_year = int(request.POST.get('year'))

            # Validate month and year
            if not (1 <= selected_month <= 12):
                raise ValueError("Invalid month")
            if not (2020 <= selected_year <= today.year):
                raise ValueError("Invalid year")

            # Check if the selected period is in the future
            selected_date = date(selected_year, selected_month, 1)
            current_month_start = date(today.year, today.month, 1)

            if selected_date > current_month_start:
                raise ValueError("Cannot generate payroll for future months. Please select current month or earlier.")

            # Calculate period dates
            start_date = date(selected_year, selected_month, 1)
            last_day = monthrange(selected_year, selected_month)[1]
            end_date = date(selected_year, selected_month, last_day)

            # Calculate pay date (typically 3 days after month end)
            from datetime import timedelta
            pay_date = end_date + timedelta(days=3)

            # Create or get payroll period
            period_name = f"{start_date.strftime('%B %Y')} Payroll"
            payroll_period, created = PayrollPeriod.objects.get_or_create(
                start_date=start_date,
                end_date=end_date,
                defaults={
                    'name': period_name,
                    'period_type': 'MONTHLY',
                    'pay_date': pay_date,
                    'status': 'DRAFT',
                    'created_by': request.user  # Use current admin user
                }
            )

            # Get all active employees with salary structures
            employees = Employee.objects.filter(
                is_active=True,
                salary_structure__is_active=True
            ).select_related('salary_structure', 'department', 'job_title')

            if not employees.exists():
                context['error'] = 'No active employees with salary structures found.'
                return render(request, 'payroll/payroll_generation.html', context)

            # Initialize calculators
            nssf_calc = NSSFCalculator()
            shif_calc = SHIFCalculator()
            housing_calc = AffordableHousingLevyCalculator()
            paye_calc = PAYECalculator()

            payslips_created = 0
            payslips_updated = 0

            # Generate payslips for each employee
            for employee in employees:
                salary_structure = employee.salary_structure
                gross_salary = salary_structure.gross_salary

                # Calculate all deductions (pass employment type for contract exemptions)
                nssf_result = nssf_calc.calculate_nssf_contribution(gross_salary, employee.employment_type)
                shif_result = shif_calc.calculate_shif_contribution(gross_salary)
                housing_result = housing_calc.calculate_housing_levy(gross_salary, employee.employment_type)

                # Validate statutory deductions compliance
                validation_result = validate_statutory_deductions_compliance(
                    employee=employee,
                    nssf_contribution=nssf_result['employee_contribution'],
                    housing_levy_contribution=housing_result['employee_contribution']
                )

                # Log any compliance issues
                if not validation_result['is_compliant']:
                    for error in validation_result['errors']:
                        messages.error(request, f"Compliance Error: {error}")

                if validation_result['warnings']:
                    for warning in validation_result['warnings']:
                        messages.warning(request, f"Compliance Notice: {warning}")

                # Calculate PAYE with employee's specific deductions
                taxable_income = gross_salary - nssf_result['employee_contribution']
                paye_result = paye_calc.calculate_paye(
                    taxable_income=taxable_income,
                    insurance_premiums=salary_structure.life_insurance_premium +
                                     salary_structure.health_insurance_premium +
                                     salary_structure.education_insurance_premium,
                    mortgage_interest=salary_structure.mortgage_interest,
                    pension_contribution=salary_structure.pension_contribution,
                    post_retirement_medical=salary_structure.post_retirement_medical_fund
                )

                # Calculate totals
                total_deductions = (
                    nssf_result['employee_contribution'] +
                    shif_result['shif_contribution'] +
                    housing_result['employee_contribution'] +
                    paye_result['paye_tax']
                )

                net_pay = gross_salary - total_deductions

                # Create or update payslip
                payslip, created = Payslip.objects.update_or_create(
                    payroll_period=payroll_period,
                    employee=employee,
                    defaults={
                        'basic_salary': salary_structure.basic_salary,
                        'house_allowance': salary_structure.house_allowance,
                        'transport_allowance': salary_structure.transport_allowance,
                        'medical_allowance': salary_structure.medical_allowance,
                        'lunch_allowance': salary_structure.lunch_allowance,
                        'communication_allowance': salary_structure.communication_allowance,
                        'other_allowances': salary_structure.other_allowances,
                        'car_benefit': salary_structure.car_benefit_value,
                        'housing_benefit': salary_structure.housing_benefit_value,
                        'gross_pay': gross_salary,
                        'paye_tax': paye_result['paye_tax'],
                        'nssf_employee': nssf_result['employee_contribution'],
                        'nssf_employer': nssf_result['employer_contribution'],
                        'shif_contribution': shif_result['shif_contribution'],
                        'housing_levy_employee': housing_result['employee_contribution'],
                        'housing_levy_employer': housing_result['employer_contribution'],
                        'total_deductions': total_deductions,
                        'net_pay': net_pay,
                        'personal_relief': paye_result['tax_reliefs']['personal_relief'],
                        'insurance_relief': paye_result['tax_reliefs']['insurance_relief'],
                    }
                )

                if created:
                    payslips_created += 1
                else:
                    payslips_updated += 1

            # Update payroll period status
            if payroll_period.status == 'DRAFT':
                payroll_period.status = 'PROCESSED'
                payroll_period.save()

            # Create or update payroll summary
            total_gross = sum(p.gross_pay for p in payroll_period.payslips.all())
            total_net = sum(p.net_pay for p in payroll_period.payslips.all())

            summary, created = PayrollSummary.objects.update_or_create(
                payroll_period=payroll_period,
                defaults={
                    'total_employees': employees.count(),
                    'total_gross_pay': total_gross,
                    'total_net_pay': total_net,
                    'total_deductions': total_gross - total_net,
                }
            )

            context.update({
                'success': True,
                'payroll_period': payroll_period,
                'payslips_created': payslips_created,
                'payslips_updated': payslips_updated,
                'total_employees': employees.count(),
                'selected_month': selected_month,
                'selected_year': selected_year,
            })

        except ValueError as e:
            context['error'] = f'Invalid input: {str(e)}'
        except Exception as e:
            context['error'] = f'Error generating payroll: {str(e)}'

    return render(request, 'payroll/payroll_generation.html', context)


@staff_member_required
def payroll_periods(request):
    """List all payroll periods - Admin only"""
    periods = PayrollPeriod.objects.all().order_by('-start_date')

    # Get organization data
    from employees.models import Organization
    organization = Organization.objects.filter(is_active=True).first()

    context = {
        'periods': periods,
        'organization': organization,
    }

    return render(request, 'payroll/payroll_periods.html', context)


@staff_member_required
def payroll_period_detail(request, period_id):
    """View detailed payroll period information with all employee payslips"""
    period = get_object_or_404(PayrollPeriod, id=period_id)
    payslips = period.payslips.select_related('employee', 'employee__department').order_by('employee__payroll_number')

    # Calculate summary statistics
    total_employees = payslips.count()
    total_gross = payslips.aggregate(total=Sum('basic_salary'))['total'] or 0
    total_net = payslips.aggregate(total=Sum('net_pay'))['total'] or 0
    total_deductions = payslips.aggregate(total=Sum('total_deductions'))['total'] or 0

    # Group by department for better organization
    departments = {}
    for payslip in payslips:
        dept_name = payslip.employee.department.name if payslip.employee.department else 'No Department'
        if dept_name not in departments:
            departments[dept_name] = []
        departments[dept_name].append(payslip)

    # Get organization data
    from employees.models import Organization
    organization = Organization.objects.filter(is_active=True).first()

    context = {
        'period': period,
        'payslips': payslips,
        'departments': departments,
        'total_employees': total_employees,
        'total_gross': total_gross,
        'total_net': total_net,
        'total_deductions': total_deductions,
        'organization': organization,
    }

    return render(request, 'payroll/payroll_period_detail.html', context)


@staff_member_required
def download_period_payslips(request, period_id):
    """Download all payslips for a period as PDF or Excel"""
    period = get_object_or_404(PayrollPeriod, id=period_id)
    download_format = request.GET.get('format', 'pdf')

    if download_format == 'excel':
        return download_period_excel(request, period)
    else:
        return download_period_pdf(request, period)


def download_period_excel(request, period):
    """Generate Excel file with all payroll data for the period - TEMPORARILY DISABLED"""
    # Temporarily disabled - requires xlsxwriter dependency
    from django.http import HttpResponse
    response = HttpResponse("Excel export temporarily disabled during deployment. Please use individual payslip downloads.", content_type='text/plain')
    return response

def download_period_excel_original(request, period):
    """Original function - temporarily disabled"""
    # Create a workbook and add a worksheet
    output = io.BytesIO()
    # workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet(f'Payroll_{period.name}')

    # Set page orientation to landscape
    worksheet.set_landscape()
    worksheet.set_paper(9)  # A4 paper size
    worksheet.fit_to_pages(1, 0)  # Fit to 1 page wide, unlimited pages tall

    # Define formats
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#4472C4',
        'font_color': 'white',
        'border': 1,
        'align': 'center'
    })

    currency_format = workbook.add_format({
        'num_format': '#,##0.00',
        'border': 1
    })

    text_format = workbook.add_format({
        'border': 1,
        'align': 'left'
    })

    center_format = workbook.add_format({
        'border': 1,
        'align': 'center'
    })

    # Get organization data
    from employees.models import Organization
    organization = Organization.objects.filter(is_active=True).first()

    # Enhanced title formats
    title_format = workbook.add_format({
        'bold': True,
        'font_size': 20,
        'align': 'center'
    })

    org_name_format = workbook.add_format({
        'bold': True,
        'font_size': 18,
        'align': 'center'
    })

    org_format = workbook.add_format({
        'font_size': 14,
        'align': 'center'
    })

    # Add organization header
    current_row = 1
    if organization:
        # Organization name
        worksheet.merge_range(f'A{current_row}:O{current_row}', organization.name, org_name_format)
        current_row += 1

        # Complete address
        address_parts = []
        if organization.address_line_1:
            address_parts.append(organization.address_line_1)
        if organization.address_line_2:
            address_parts.append(organization.address_line_2)
        if organization.city:
            address_parts.append(organization.city)
        if organization.postal_code:
            address_parts.append(f"P.O. Box {organization.postal_code}")
        if organization.country:
            address_parts.append(organization.country)

        if address_parts:
            full_address = ", ".join(address_parts)
            worksheet.merge_range(f'A{current_row}:O{current_row}', full_address, org_format)
            current_row += 1

        # Contact information
        contact_info = []
        if organization.phone_number:
            contact_info.append(f"Tel: {organization.phone_number}")
        if organization.email:
            contact_info.append(f"Email: {organization.email}")
        if organization.website:
            contact_info.append(f"Web: {organization.website}")

        if contact_info:
            worksheet.merge_range(f'A{current_row}:O{current_row}', " | ".join(contact_info), org_format)
            current_row += 1

        # KRA PIN
        if organization.kra_pin:
            worksheet.merge_range(f'A{current_row}:O{current_row}', f"KRA PIN: {organization.kra_pin}", org_format)
            current_row += 1

        current_row += 1  # Add space

    # Report title and period info
    worksheet.merge_range(f'A{current_row}:O{current_row}', f'PAYROLL REPORT - {period.name}', title_format)
    current_row += 1
    worksheet.merge_range(f'A{current_row}:O{current_row}', f'Period: {period.start_date.strftime("%B %d, %Y")} - {period.end_date.strftime("%B %d, %Y")}', org_format)
    current_row += 1

    # Headers
    headers = [
        'Employee Name', 'Payroll Number', 'Department', 'Job Title',
        'Basic Salary', 'Allowances', 'Gross Pay', 'PAYE', 'NSSF Employee',
        'SHIF', 'Housing Levy', 'Total Deductions', 'Net Pay',
        'NSSF Employer', 'Housing Levy Employer'
    ]

    # Write headers
    for col, header in enumerate(headers):
        worksheet.write(current_row, col, header, header_format)

    # Get payslips data
    payslips = period.payslips.select_related('employee', 'employee__department', 'employee__job_title').order_by('employee__payroll_number')

    # Write data
    row = current_row + 1
    for payslip in payslips:
        worksheet.write(row, 0, payslip.employee.full_name, text_format)
        worksheet.write(row, 1, payslip.employee.payroll_number, center_format)
        worksheet.write(row, 2, payslip.employee.department.name if payslip.employee.department else 'N/A', text_format)
        worksheet.write(row, 3, payslip.employee.job_title.title if payslip.employee.job_title else 'N/A', text_format)
        worksheet.write(row, 4, float(payslip.basic_salary), currency_format)
        worksheet.write(row, 5, float(payslip.total_allowances), currency_format)
        worksheet.write(row, 6, float(payslip.gross_pay), currency_format)
        worksheet.write(row, 7, float(payslip.paye_tax), currency_format)
        worksheet.write(row, 8, float(payslip.nssf_employee), currency_format)
        worksheet.write(row, 9, float(payslip.shif_contribution), currency_format)
        worksheet.write(row, 10, float(payslip.housing_levy_employee), currency_format)
        worksheet.write(row, 11, float(payslip.total_deductions), currency_format)
        worksheet.write(row, 12, float(payslip.net_pay), currency_format)
        worksheet.write(row, 13, float(payslip.nssf_employer), currency_format)
        worksheet.write(row, 14, float(payslip.housing_levy_employer), currency_format)
        row += 1

    # Add totals row
    total_row = row + 1
    worksheet.write(total_row, 0, 'TOTALS', header_format)
    worksheet.merge_range(total_row, 1, total_row, 3, '', header_format)

    # Calculate totals
    total_basic = sum(float(p.basic_salary) for p in payslips)
    total_allowances = sum(float(p.total_allowances) for p in payslips)
    total_gross = sum(float(p.gross_pay) for p in payslips)
    total_paye = sum(float(p.paye_tax) for p in payslips)
    total_nssf_emp = sum(float(p.nssf_employee) for p in payslips)
    total_shif = sum(float(p.shif_contribution) for p in payslips)
    total_housing_emp = sum(float(p.housing_levy_employee) for p in payslips)
    total_deductions = sum(float(p.total_deductions) for p in payslips)
    total_net = sum(float(p.net_pay) for p in payslips)
    total_nssf_employer = sum(float(p.nssf_employer) for p in payslips)
    total_housing_employer = sum(float(p.housing_levy_employer) for p in payslips)

    # Write totals
    totals = [total_basic, total_allowances, total_gross, total_paye, total_nssf_emp,
              total_shif, total_housing_emp, total_deductions, total_net,
              total_nssf_employer, total_housing_employer]

    for col, total in enumerate(totals, start=4):
        worksheet.write(total_row, col, total, currency_format)

    # Set column widths optimized for landscape
    worksheet.set_column('A:A', 18)  # Employee Name
    worksheet.set_column('B:B', 12)  # Payroll Number
    worksheet.set_column('C:C', 14)  # Department
    worksheet.set_column('D:D', 16)  # Job Title
    worksheet.set_column('E:O', 11)  # All currency columns

    # Set print options for landscape
    worksheet.set_margins(left=0.5, right=0.5, top=0.75, bottom=0.75)
    worksheet.set_header('&C&"Arial,Bold"&14' + f'Payroll Report - {period.name}')
    worksheet.set_footer('&L&D &T&R&P of &N')  # Date, time on left; page numbers on right

    workbook.close()
    output.seek(0)

    # Create response
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="Payroll_{period.name}_{timezone.now().strftime("%Y%m%d")}.xlsx"'

    return response


def download_period_pdf(request, period):
    """Generate PDF file with all payslips for the period - TEMPORARILY DISABLED"""
    # Temporarily disabled - requires reportlab dependency
    from django.http import HttpResponse
    response = HttpResponse("PDF export temporarily disabled during deployment. Please use individual payslip downloads.", content_type='text/plain')
    return response

def download_period_pdf_original(request, period):
    """Original function - temporarily disabled"""
    # Create a file-like buffer to receive PDF data
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file" with landscape orientation
    # doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), rightMargin=36, leftMargin=36, topMargin=72, bottomMargin=18)

    # Temporarily disabled - requires reportlab
    return HttpResponse("PDF export temporarily disabled during deployment.", content_type='text/plain')


@staff_member_required
def payroll_period_delete(request, period_id):
    """Delete a single payroll period - Admin only"""
    period = get_object_or_404(PayrollPeriod, id=period_id)

    if request.method == 'POST':
        period_name = period.name
        payslip_count = period.payslips.count()

        # Delete the period (this will cascade delete payslips)
        period.delete()

        messages.success(
            request,
            f'Payroll period "{period_name}" and {payslip_count} associated payslips have been deleted successfully.'
        )
        return redirect('payroll_processing:payroll_periods')

    # Get organization data for template
    from employees.models import Organization
    organization = Organization.objects.filter(is_active=True).first()

    context = {
        'period': period,
        'payslip_count': period.payslips.count(),
        'title': f'Delete Payroll Period - {period.name}',
        'organization': organization,
    }
    return render(request, 'payroll/payroll_period_delete.html', context)


@staff_member_required
def bulk_payroll_period_delete(request):
    """Bulk delete payroll periods - Admin only"""
    if request.method == 'POST':
        period_ids = request.POST.getlist('period_ids')

        if not period_ids:
            messages.error(request, 'No payroll periods selected for deletion.')
            return redirect('payroll_processing:payroll_periods')

        try:
            # Get period information for confirmation message
            periods = PayrollPeriod.objects.filter(id__in=period_ids)
            period_names = [period.name for period in periods]
            total_payslips = sum(period.payslips.count() for period in periods)
            count = periods.count()

            # Delete the periods (this will cascade delete payslips)
            periods.delete()

            if count == 1:
                messages.success(
                    request,
                    f'Payroll period "{period_names[0]}" and {total_payslips} associated payslips have been deleted successfully.'
                )
            else:
                messages.success(
                    request,
                    f'{count} payroll periods and {total_payslips} associated payslips have been deleted successfully.'
                )

        except Exception as e:
            messages.error(request, f'Error deleting payroll periods: {str(e)}')

    return redirect('payroll_processing:payroll_periods')
