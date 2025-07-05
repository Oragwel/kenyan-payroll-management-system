"""
Utility functions for calculating Kenyan statutory deductions
"""
from decimal import Decimal, ROUND_HALF_UP
from datetime import date
from .models import PAYETaxBand, TaxRelief, NSSFRate, SHIFRate, AffordableHousingLevyRate


def validate_statutory_deductions_compliance(employee, nssf_contribution, housing_levy_contribution):
    """
    Validate that statutory deductions comply with Kenyan employment law

    Args:
        employee: Employee instance
        nssf_contribution: Calculated NSSF contribution amount
        housing_levy_contribution: Calculated Housing Levy contribution amount

    Returns:
        dict: Validation results with compliance status

    Raises:
        ValueError: If mandatory deductions are missing for any employment type
    """
    validation_results = {
        'is_compliant': True,
        'errors': [],
        'warnings': [],
        'employment_type': employee.employment_type
    }

    # NSSF Validation - Mandatory for ALL employment types EXCEPT CONTRACT
    if employee.employment_type != 'CONTRACT':
        if nssf_contribution <= 0:
            validation_results['is_compliant'] = False
            validation_results['errors'].append(
                f"NSSF contribution is mandatory for {employee.employment_type} employees. "
                f"Employee {employee.payroll_number} missing NSSF deduction."
            )
    else:
        # Contract employees are exempt from NSSF
        if nssf_contribution > 0:
            validation_results['warnings'].append(
                f"Contract employee {employee.payroll_number} should not have NSSF deductions. "
                "Only SHIF is mandatory for contract employees."
            )

    # Housing Levy Validation - Mandatory for ALL employment types EXCEPT CONTRACT
    if employee.employment_type != 'CONTRACT':
        if housing_levy_contribution <= 0:
            validation_results['is_compliant'] = False
            validation_results['errors'].append(
                f"Housing Levy is mandatory for {employee.employment_type} employees. "
                f"Employee {employee.payroll_number} missing Housing Levy deduction."
            )
    else:
        # Contract employees are exempt from Housing Levy
        if housing_levy_contribution > 0:
            validation_results['warnings'].append(
                f"Contract employee {employee.payroll_number} should not have Housing Levy deductions. "
                "Only SHIF is mandatory for contract employees."
            )

    # Additional validation for casual workers (common misconception)
    if employee.employment_type == 'CASUAL':
        if nssf_contribution <= 0 or housing_levy_contribution <= 0:
            validation_results['warnings'].append(
                "REMINDER: Both NSSF and Housing Levy are mandatory for casual workers "
                "as per NSSF Act 2013 and KRA Housing Levy regulations."
            )

    # Contract employee specific validation
    if employee.employment_type == 'CONTRACT':
        validation_results['warnings'].append(
            f"Contract employee {employee.payroll_number}: Only SHIF deductions apply. "
            "NSSF and Housing Levy are not deducted for contract employees."
        )

    return validation_results


class PAYECalculator:
    """
    PAYE (Pay As You Earn) tax calculator for Kenya
    Based on KRA tax bands and regulations
    """
    
    def __init__(self, calculation_date=None):
        """
        Initialize PAYE calculator with effective date
        
        Args:
            calculation_date: Date for which to calculate PAYE (defaults to today)
        """
        self.calculation_date = calculation_date or date.today()
        self.tax_bands = self._get_active_tax_bands()
        self.personal_relief = self._get_personal_relief()
    
    def _get_active_tax_bands(self):
        """Get active PAYE tax bands for the calculation date"""
        return PAYETaxBand.objects.filter(
            effective_date__lte=self.calculation_date,
            is_active=True
        ).order_by('lower_limit')
    
    def _get_personal_relief(self):
        """Get personal relief amount for the calculation date"""
        try:
            relief = TaxRelief.objects.filter(
                relief_type='PERSONAL',
                effective_date__lte=self.calculation_date,
                is_active=True
            ).order_by('-effective_date').first()
            return relief.amount if relief else Decimal('2400')  # Default KES 2,400
        except:
            return Decimal('2400')  # Default KES 2,400
    
    def calculate_paye(self, taxable_income, insurance_premiums=None, 
                      mortgage_interest=None, pension_contribution=None,
                      post_retirement_medical=None):
        """
        Calculate PAYE tax for given taxable income
        
        Args:
            taxable_income: Monthly taxable income
            insurance_premiums: Life/health/education insurance premiums
            mortgage_interest: Monthly mortgage interest (max KES 30,000)
            pension_contribution: Monthly pension contribution (max KES 30,000)
            post_retirement_medical: Post-retirement medical fund (max KES 15,000)
        
        Returns:
            dict: Contains tax calculation breakdown
        """
        # Convert to Decimal for precision
        taxable_income = Decimal(str(taxable_income))
        
        # Calculate allowable deductions
        deductions = self._calculate_allowable_deductions(
            insurance_premiums, mortgage_interest, 
            pension_contribution, post_retirement_medical
        )
        
        # Apply deductions to taxable income
        income_after_deductions = max(Decimal('0'), taxable_income - deductions['total'])
        
        # Calculate tax before relief
        tax_before_relief = self._calculate_tax_on_income(income_after_deductions)
        
        # Calculate tax reliefs
        reliefs = self._calculate_tax_reliefs(insurance_premiums)
        
        # Calculate final PAYE
        paye_tax = max(Decimal('0'), tax_before_relief - reliefs['total'])
        
        return {
            'taxable_income': taxable_income,
            'allowable_deductions': deductions,
            'income_after_deductions': income_after_deductions,
            'tax_before_relief': tax_before_relief,
            'tax_reliefs': reliefs,
            'paye_tax': paye_tax.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            'effective_tax_rate': (paye_tax / taxable_income * 100) if taxable_income > 0 else Decimal('0')
        }
    
    def _calculate_allowable_deductions(self, insurance_premiums=None, 
                                      mortgage_interest=None, pension_contribution=None,
                                      post_retirement_medical=None):
        """Calculate allowable deductions from taxable income"""
        deductions = {
            'mortgage_interest': Decimal('0'),
            'pension_contribution': Decimal('0'),
            'post_retirement_medical': Decimal('0'),
            'total': Decimal('0')
        }
        
        # Mortgage interest relief (max KES 30,000 per month)
        if mortgage_interest:
            mortgage_interest = Decimal(str(mortgage_interest))
            deductions['mortgage_interest'] = min(mortgage_interest, Decimal('30000'))
        
        # Pension contribution (max KES 30,000 per month)
        if pension_contribution:
            pension_contribution = Decimal(str(pension_contribution))
            deductions['pension_contribution'] = min(pension_contribution, Decimal('30000'))
        
        # Post-retirement medical fund (max KES 15,000 per month)
        if post_retirement_medical:
            post_retirement_medical = Decimal(str(post_retirement_medical))
            deductions['post_retirement_medical'] = min(post_retirement_medical, Decimal('15000'))
        
        deductions['total'] = (
            deductions['mortgage_interest'] + 
            deductions['pension_contribution'] + 
            deductions['post_retirement_medical']
        )
        
        return deductions
    
    def _calculate_tax_on_income(self, income):
        """Calculate tax on income using progressive tax bands"""
        if income <= 0:
            return Decimal('0')
        
        total_tax = Decimal('0')
        remaining_income = income
        
        for band in self.tax_bands:
            if remaining_income <= 0:
                break
            
            # Determine the taxable amount in this band
            band_lower = band.lower_limit
            band_upper = band.upper_limit or Decimal('999999999')  # No upper limit for highest band
            
            if income <= band_lower:
                continue  # Income doesn't reach this band
            
            # Calculate taxable amount in this band
            taxable_in_band = min(remaining_income, band_upper - band_lower)
            if income > band_upper:
                taxable_in_band = band_upper - band_lower
            else:
                taxable_in_band = income - band_lower
            
            # Calculate tax for this band
            band_tax = taxable_in_band * (band.tax_rate / Decimal('100'))
            total_tax += band_tax
            
            remaining_income -= taxable_in_band
        
        return total_tax
    
    def _calculate_tax_reliefs(self, insurance_premiums=None):
        """Calculate tax reliefs"""
        reliefs = {
            'personal_relief': self.personal_relief,
            'insurance_relief': Decimal('0'),
            'total': Decimal('0')
        }
        
        # Insurance relief (15% of premiums, max KES 60,000 per year = KES 5,000 per month)
        if insurance_premiums:
            insurance_premiums = Decimal(str(insurance_premiums))
            annual_premiums = insurance_premiums * 12
            max_annual_relief = Decimal('60000')
            annual_relief = min(annual_premiums * Decimal('0.15'), max_annual_relief)
            reliefs['insurance_relief'] = annual_relief / 12  # Monthly relief
        
        reliefs['total'] = reliefs['personal_relief'] + reliefs['insurance_relief']
        
        return reliefs
    
    def get_tax_bands_info(self):
        """Get information about current tax bands"""
        bands_info = []
        for band in self.tax_bands:
            bands_info.append({
                'lower_limit': band.lower_limit,
                'upper_limit': band.upper_limit,
                'tax_rate': band.tax_rate,
                'description': str(band)
            })
        return bands_info


def calculate_annual_paye(monthly_taxable_income, **kwargs):
    """
    Calculate annual PAYE tax
    
    Args:
        monthly_taxable_income: Monthly taxable income
        **kwargs: Additional parameters for PAYE calculation
    
    Returns:
        dict: Annual PAYE calculation breakdown
    """
    calculator = PAYECalculator()
    monthly_calculation = calculator.calculate_paye(monthly_taxable_income, **kwargs)
    
    # Convert monthly amounts to annual
    annual_calculation = {}
    for key, value in monthly_calculation.items():
        if isinstance(value, dict):
            annual_calculation[key] = {}
            for sub_key, sub_value in value.items():
                if isinstance(sub_value, Decimal):
                    annual_calculation[key][sub_key] = sub_value * 12
                else:
                    annual_calculation[key][sub_key] = sub_value
        elif isinstance(value, Decimal) and key != 'effective_tax_rate':
            annual_calculation[key] = value * 12
        else:
            annual_calculation[key] = value
    
    return annual_calculation


class NSSFCalculator:
    """
    NSSF (National Social Security Fund) contribution calculator for Kenya
    Based on NSSF Act 2013 and current rates

    IMPORTANT: NSSF contributions are MANDATORY for permanent, casual, and intern employees.
    CONTRACT employees are EXEMPT from NSSF contributions.
    Only SHIF is mandatory for contract employees.
    """

    def __init__(self, calculation_date=None):
        """
        Initialize NSSF calculator with effective date

        Args:
            calculation_date: Date for which to calculate NSSF (defaults to today)
        """
        self.calculation_date = calculation_date or date.today()
        self.nssf_rates = self._get_active_nssf_rates()

    def _get_active_nssf_rates(self):
        """Get active NSSF rates for the calculation date"""
        return NSSFRate.objects.filter(
            effective_date__lte=self.calculation_date,
            is_active=True
        ).order_by('tier', 'lower_limit')

    def is_nssf_applicable(self, employment_type):
        """
        Check if NSSF contributions apply to the employment type

        Args:
            employment_type: Employee's employment type

        Returns:
            bool: True if NSSF applies, False for contract employees
        """
        return employment_type != 'CONTRACT'

    def calculate_nssf_contribution(self, gross_salary, employment_type=None):
        """
        Calculate NSSF contribution for employee and employer

        Args:
            gross_salary: Monthly gross salary
            employment_type: Employee's employment type (optional)

        Returns:
            dict: Contains NSSF contribution breakdown
        """
        gross_salary = Decimal(str(gross_salary))

        # Check if NSSF applies to this employment type
        if employment_type and not self.is_nssf_applicable(employment_type):
            return {
                'gross_salary': gross_salary,
                'tier_1_contribution': Decimal('0'),
                'tier_2_contribution': Decimal('0'),
                'employee_contribution': Decimal('0'),
                'employer_contribution': Decimal('0'),
                'total_contribution': Decimal('0'),
                'exemption_reason': f'Contract employees are exempt from NSSF contributions',
                'applicable': False
            }

        if gross_salary <= 0:
            return {
                'gross_salary': gross_salary,
                'tier_1_contribution': Decimal('0'),
                'tier_2_contribution': Decimal('0'),
                'employee_contribution': Decimal('0'),
                'employer_contribution': Decimal('0'),
                'total_contribution': Decimal('0'),
                'contribution_breakdown': []
            }

        tier_1_contribution = Decimal('0')
        tier_2_contribution = Decimal('0')
        breakdown = []

        for rate in self.nssf_rates:
            if rate.tier == 1:
                # Tier 1: First KES 7,000 at 6%
                tier_1_pensionable = min(gross_salary, rate.upper_limit)
                tier_1_contribution = tier_1_pensionable * (rate.contribution_rate / Decimal('100'))
                breakdown.append({
                    'tier': 1,
                    'pensionable_amount': tier_1_pensionable,
                    'rate': rate.contribution_rate,
                    'employee_contribution': tier_1_contribution,
                    'employer_contribution': tier_1_contribution
                })

            elif rate.tier == 2 and gross_salary > rate.lower_limit - 1:
                # Tier 2: Excess above KES 7,000 up to KES 36,000 at 6%
                tier_2_pensionable = min(
                    max(gross_salary - (rate.lower_limit - 1), Decimal('0')),
                    rate.upper_limit - (rate.lower_limit - 1)
                )
                tier_2_contribution = tier_2_pensionable * (rate.contribution_rate / Decimal('100'))
                breakdown.append({
                    'tier': 2,
                    'pensionable_amount': tier_2_pensionable,
                    'rate': rate.contribution_rate,
                    'employee_contribution': tier_2_contribution,
                    'employer_contribution': tier_2_contribution
                })

        # Calculate totals
        employee_contribution = tier_1_contribution + tier_2_contribution
        employer_contribution = employee_contribution  # Employer matches employee contribution
        total_contribution = employee_contribution + employer_contribution

        return {
            'gross_salary': gross_salary,
            'tier_1_contribution': tier_1_contribution.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            'tier_2_contribution': tier_2_contribution.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            'employee_contribution': employee_contribution.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            'employer_contribution': employer_contribution.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            'total_contribution': total_contribution.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            'contribution_breakdown': breakdown,
            'applicable': True
        }

    def get_nssf_rates_info(self):
        """Get information about current NSSF rates"""
        rates_info = []
        for rate in self.nssf_rates:
            rates_info.append({
                'tier': rate.tier,
                'lower_limit': rate.lower_limit,
                'upper_limit': rate.upper_limit,
                'contribution_rate': rate.contribution_rate,
                'description': str(rate)
            })
        return rates_info


class SHIFCalculator:
    """
    SHIF (Social Health Insurance Fund) contribution calculator for Kenya

    SHIF replaced NHIF in 2024 as part of Kenya's Universal Health Coverage (UHC) reforms.
    Unlike NHIF's fixed contribution bands, SHIF uses a percentage-based system (2.75% of gross salary)
    with a minimum contribution of KES 300 per month.
    """

    def __init__(self, calculation_date=None):
        """
        Initialize SHIF calculator with effective date

        Args:
            calculation_date: Date for which to calculate SHIF (defaults to today)
        """
        self.calculation_date = calculation_date or date.today()
        self.shif_rate = self._get_active_shif_rate()

    def _get_active_shif_rate(self):
        """Get active SHIF rate for the calculation date"""
        return SHIFRate.objects.filter(
            effective_date__lte=self.calculation_date,
            is_active=True
        ).order_by('-effective_date').first()

    def calculate_shif_contribution(self, gross_salary):
        """
        Calculate SHIF contribution (2.75% of gross salary, minimum KES 300)

        Args:
            gross_salary: Monthly gross salary

        Returns:
            dict: Contains SHIF contribution details
        """
        gross_salary = Decimal(str(gross_salary))

        if not self.shif_rate or gross_salary <= 0:
            return {
                'gross_salary': gross_salary,
                'shif_contribution': Decimal('0'),
                'contribution_rate': Decimal('0'),
                'minimum_contribution': Decimal('0')
            }

        # Calculate 2.75% of gross salary
        calculated_contribution = gross_salary * (self.shif_rate.contribution_rate / Decimal('100'))

        # Apply minimum contribution
        shif_contribution = max(calculated_contribution, self.shif_rate.minimum_contribution)

        return {
            'gross_salary': gross_salary,
            'shif_contribution': shif_contribution.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            'contribution_rate': self.shif_rate.contribution_rate,
            'minimum_contribution': self.shif_rate.minimum_contribution,
            'calculated_contribution': calculated_contribution.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        }


class AffordableHousingLevyCalculator:
    """
    Affordable Housing Levy calculator for Kenya
    1.5% each for employee and employer (total 3%)

    IMPORTANT: Housing Levy is MANDATORY for permanent, casual, and intern employees.
    CONTRACT employees are EXEMPT from Housing Levy contributions.
    Only SHIF is mandatory for contract employees.
    """

    def __init__(self, calculation_date=None):
        """
        Initialize Housing Levy calculator with effective date

        Args:
            calculation_date: Date for which to calculate levy (defaults to today)
        """
        self.calculation_date = calculation_date or date.today()
        self.levy_rate = self._get_active_levy_rate()

    def _get_active_levy_rate(self):
        """Get active Housing Levy rate for the calculation date"""
        return AffordableHousingLevyRate.objects.filter(
            effective_date__lte=self.calculation_date,
            is_active=True
        ).order_by('-effective_date').first()

    def is_housing_levy_applicable(self, employment_type):
        """
        Check if Housing Levy contributions apply to the employment type

        Args:
            employment_type: Employee's employment type

        Returns:
            bool: True if Housing Levy applies, False for contract employees
        """
        return employment_type != 'CONTRACT'

    def calculate_housing_levy(self, gross_salary, employment_type=None):
        """
        Calculate Affordable Housing Levy (1.5% each for employee and employer)

        Args:
            gross_salary: Monthly gross salary
            employment_type: Employee's employment type (optional)

        Returns:
            dict: Contains Housing Levy contribution details
        """
        gross_salary = Decimal(str(gross_salary))

        # Check if Housing Levy applies to this employment type
        if employment_type and not self.is_housing_levy_applicable(employment_type):
            return {
                'gross_salary': gross_salary,
                'employee_contribution': Decimal('0'),
                'employer_contribution': Decimal('0'),
                'total_contribution': Decimal('0'),
                'exemption_reason': f'Contract employees are exempt from Housing Levy contributions',
                'applicable': False
            }

        if not self.levy_rate or gross_salary <= 0:
            return {
                'gross_salary': gross_salary,
                'employee_contribution': Decimal('0'),
                'employer_contribution': Decimal('0'),
                'total_contribution': Decimal('0'),
                'employee_rate': Decimal('0'),
                'employer_rate': Decimal('0')
            }

        # Calculate contributions
        employee_contribution = gross_salary * (self.levy_rate.employee_rate / Decimal('100'))
        employer_contribution = gross_salary * (self.levy_rate.employer_rate / Decimal('100'))
        total_contribution = employee_contribution + employer_contribution

        return {
            'gross_salary': gross_salary,
            'employee_contribution': employee_contribution.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            'employer_contribution': employer_contribution.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            'total_contribution': total_contribution.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            'employee_rate': self.levy_rate.employee_rate,
            'employer_rate': self.levy_rate.employer_rate,
            'applicable': True
        }
