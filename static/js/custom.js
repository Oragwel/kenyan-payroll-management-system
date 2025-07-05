// Kenyan Payroll System Custom JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Format currency inputs
    const currencyInputs = document.querySelectorAll('input[type="number"]');
    currencyInputs.forEach(function(input) {
        input.addEventListener('blur', function() {
            if (this.value) {
                this.value = parseFloat(this.value).toFixed(2);
            }
        });
    });

    // KRA PIN validation
    const kraPinInputs = document.querySelectorAll('input[name*="kra_pin"]');
    kraPinInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            const value = this.value.toUpperCase();
            const pattern = /^[A-Z]\d{9}[A-Z]$/;
            
            if (value && !pattern.test(value)) {
                this.classList.add('is-invalid');
                showFieldError(this, 'KRA PIN must be in format: A123456789B');
            } else {
                this.classList.remove('is-invalid');
                hideFieldError(this);
            }
        });
    });

    // Phone number validation
    const phoneInputs = document.querySelectorAll('input[name*="phone"]');
    phoneInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            const value = this.value.replace(/\s+/g, '');
            const pattern = /^(\+254|0)[17]\d{8}$/;
            
            if (value && !pattern.test(value)) {
                this.classList.add('is-invalid');
                showFieldError(this, 'Please enter a valid Kenyan phone number');
            } else {
                this.classList.remove('is-invalid');
                hideFieldError(this);
            }
        });
    });

    // Real-time payroll calculation
    const salaryInputs = document.querySelectorAll('.salary-input');
    salaryInputs.forEach(function(input) {
        input.addEventListener('input', debounce(calculatePayroll, 500));
    });

    // Employment type change handler
    const employmentTypeSelect = document.getElementById('employment_type');
    if (employmentTypeSelect) {
        employmentTypeSelect.addEventListener('change', function() {
            updateDeductionInfo(this.value);
            // Trigger calculation if there are salary values
            const basicSalary = parseFloat(document.getElementById('basic_salary')?.value || 0);
            const allowances = parseFloat(document.getElementById('allowances')?.value || 0);
            if (basicSalary > 0 || allowances > 0) {
                calculatePayroll();
            }
        });

        // Initialize on page load
        updateDeductionInfo(employmentTypeSelect.value);
    }
});

// Utility Functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-KE', {
        style: 'currency',
        currency: 'KES',
        minimumFractionDigits: 2
    }).format(amount);
}

function formatNumber(number) {
    return new Intl.NumberFormat('en-KE').format(number);
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function showFieldError(field, message) {
    let errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        field.parentNode.appendChild(errorDiv);
    }
    errorDiv.textContent = message;
}

function hideFieldError(field) {
    const errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// Payroll Calculation Functions
function calculatePayroll() {
    const grossSalary = parseFloat(document.getElementById('gross_salary')?.value || 0);

    if (grossSalary <= 0) {
        clearResults();
        return;
    }

    // Show loading
    showLoading();

    // Get additional inputs for tax relief
    const insurancePremiums = parseFloat(document.getElementById('insurance_premiums')?.value || 0);
    const mortgageInterest = parseFloat(document.getElementById('mortgage_interest')?.value || 0);
    const pensionContribution = parseFloat(document.getElementById('pension_contribution')?.value || 0);
    const medicalFund = parseFloat(document.getElementById('medical_fund')?.value || 0);
    const employmentType = document.getElementById('employment_type')?.value || 'PERMANENT';

    // Use AJAX for server-side calculation if available
    if (window.location.pathname.includes('calculator')) {
        fetch('/payroll/calculate-ajax/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: new URLSearchParams({
                gross_salary: grossSalary,
                employment_type: employmentType,
                insurance_premiums: insurancePremiums,
                mortgage_interest: mortgageInterest,
                pension_contribution: pensionContribution,
                post_retirement_medical: medicalFund
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            displayServerResults(data);
        })
        .catch(error => {
            console.error('Server calculation failed, using client-side:', error);
            // Fallback to client-side calculation
            calculateClientSide(grossSalary, insurancePremiums, mortgageInterest, pensionContribution, medicalFund);
        });
    } else {
        // Use client-side calculation
        calculateClientSide(grossSalary, insurancePremiums, mortgageInterest, pensionContribution, medicalFund);
    }
}

function calculateClientSide(grossSalary, insurancePremiums, mortgageInterest, pensionContribution, medicalFund) {
    // Calculate NSSF
    const nssf = calculateNSSF(grossSalary);

    // Calculate SHIF
    const shif = calculateSHIF(grossSalary);

    // Calculate Housing Levy
    const housingLevy = calculateHousingLevy(grossSalary);

    // Calculate PAYE (after NSSF deduction)
    const taxableIncome = grossSalary - nssf.employee;
    const paye = calculatePAYE(taxableIncome);

    // Calculate totals
    const totalDeductions = nssf.employee + shif + housingLevy.employee + paye;
    const netPay = grossSalary - totalDeductions;

    // Display results
    displayResults({
        grossSalary,
        nssf,
        shif,
        housingLevy,
        paye,
        totalDeductions,
        netPay
    });

    hideLoading();
}

function displayServerResults(data) {
    const resultsContainer = document.getElementById('calculation-results');
    if (!resultsContainer) return;

    resultsContainer.innerHTML = `
        <div class="calculation-result">
            <h5 class="mb-3"><i class="bi bi-calculator me-2"></i>Payroll Calculation Results</h5>

            <div class="result-item">
                <span class="result-label">Gross Salary:</span>
                <span class="result-value">${formatCurrency(data.gross_salary)}</span>
            </div>

            <div class="result-item">
                <span class="result-label">NSSF (Employee):</span>
                <span class="result-value">${formatCurrency(data.nssf.employee)}${data.nssf.employee === 0 && data.nssf.exemption_reason ? ' <small class="text-muted">(Exempt)</small>' : ''}</span>
            </div>

            <div class="result-item">
                <span class="result-label">SHIF:</span>
                <span class="result-value">${formatCurrency(data.shif.contribution)}</span>
            </div>

            <div class="result-item">
                <span class="result-label">Housing Levy (Employee):</span>
                <span class="result-value">${formatCurrency(data.housing_levy.employee)}${data.housing_levy.employee === 0 && data.housing_levy.exemption_reason ? ' <small class="text-muted">(Exempt)</small>' : ''}</span>
            </div>

            <div class="result-item">
                <span class="result-label">PAYE Tax:</span>
                <span class="result-value">${formatCurrency(data.paye.tax)}</span>
            </div>

            <div class="result-item">
                <span class="result-label">Total Deductions:</span>
                <span class="result-value">${formatCurrency(data.totals.statutory_deductions)}</span>
            </div>

            <div class="result-item">
                <span class="result-label"><strong>Net Pay:</strong></span>
                <span class="result-value"><strong>${formatCurrency(data.totals.net_pay)}</strong></span>
            </div>

            <div class="result-item">
                <span class="result-label">Take-home %:</span>
                <span class="result-value">${data.totals.take_home_percentage.toFixed(1)}%</span>
            </div>
        </div>
    `;
}

function calculateNSSF(grossSalary) {
    // NSSF is MANDATORY for ALL employment types (Permanent, Contract, Casual, Intern)
    // Based on NSSF Act 2013 - NO exemptions for casual workers

    // Tier 1: First KES 7,000 at 6%
    const tier1Limit = 7000;
    const tier1Amount = Math.min(grossSalary, tier1Limit);
    const tier1Contribution = tier1Amount * 0.06;

    // Tier 2: Excess above KES 7,000 up to KES 36,000 at 6%
    const tier2Limit = 36000;
    const tier2Amount = Math.max(0, Math.min(grossSalary - tier1Limit, tier2Limit - tier1Limit));
    const tier2Contribution = tier2Amount * 0.06;

    const employeeContribution = tier1Contribution + tier2Contribution;

    return {
        employee: employeeContribution,
        employer: employeeContribution,
        total: employeeContribution * 2
    };
}

function calculateSHIF(grossSalary) {
    const rate = 0.0275; // 2.75%
    const minimum = 300;
    const calculated = grossSalary * rate;
    return Math.max(calculated, minimum);
}

function calculateHousingLevy(grossSalary) {
    // Housing Levy is MANDATORY for ALL employees regardless of employment type
    // Based on KRA notice effective March 19, 2024 - NO exemptions

    const rate = 0.015; // 1.5% employee + 1.5% employer
    const contribution = grossSalary * rate;

    return {
        employee: contribution,
        employer: contribution,
        total: contribution * 2
    };
}

function calculatePAYE(taxableIncome) {
    const personalRelief = 2400;
    
    // Tax bands
    const bands = [
        { min: 0, max: 24000, rate: 0.10 },
        { min: 24001, max: 32333, rate: 0.25 },
        { min: 32334, max: 500000, rate: 0.30 },
        { min: 500001, max: 800000, rate: 0.325 },
        { min: 800001, max: Infinity, rate: 0.35 }
    ];
    
    let tax = 0;
    let remainingIncome = taxableIncome;
    
    for (const band of bands) {
        if (remainingIncome <= 0) break;
        
        const bandWidth = band.max - band.min + 1;
        const taxableInBand = Math.min(remainingIncome, bandWidth);
        
        if (taxableIncome > band.min) {
            const actualTaxable = Math.min(taxableInBand, taxableIncome - band.min + 1);
            tax += actualTaxable * band.rate;
            remainingIncome -= actualTaxable;
        }
    }
    
    return Math.max(0, tax - personalRelief);
}

function displayResults(results) {
    const resultsContainer = document.getElementById('calculation-results');
    if (!resultsContainer) return;
    
    resultsContainer.innerHTML = `
        <div class="calculation-result">
            <h5 class="mb-3"><i class="bi bi-calculator me-2"></i>Payroll Calculation Results</h5>
            
            <div class="result-item">
                <span class="result-label">Gross Salary:</span>
                <span class="result-value">${formatCurrency(results.grossSalary)}</span>
            </div>
            
            <div class="result-item">
                <span class="result-label">NSSF (Employee):</span>
                <span class="result-value">${formatCurrency(results.nssf.employee)}</span>
            </div>
            
            <div class="result-item">
                <span class="result-label">SHIF:</span>
                <span class="result-value">${formatCurrency(results.shif)}</span>
            </div>
            
            <div class="result-item">
                <span class="result-label">Housing Levy (Employee):</span>
                <span class="result-value">${formatCurrency(results.housingLevy.employee)}</span>
            </div>
            
            <div class="result-item">
                <span class="result-label">PAYE Tax:</span>
                <span class="result-value">${formatCurrency(results.paye)}</span>
            </div>
            
            <div class="result-item">
                <span class="result-label">Total Deductions:</span>
                <span class="result-value">${formatCurrency(results.totalDeductions)}</span>
            </div>
            
            <div class="result-item">
                <span class="result-label"><strong>Net Pay:</strong></span>
                <span class="result-value"><strong>${formatCurrency(results.netPay)}</strong></span>
            </div>
        </div>
    `;
}

function clearResults() {
    const resultsContainer = document.getElementById('calculation-results');
    if (resultsContainer) {
        resultsContainer.innerHTML = '';
    }
}

function showLoading() {
    const resultsContainer = document.getElementById('calculation-results');
    if (resultsContainer) {
        resultsContainer.innerHTML = `
            <div class="text-center py-4">
                <div class="loading"></div>
                <p class="mt-2 text-muted">Calculating...</p>
            </div>
        `;
    }
}

function hideLoading() {
    // Loading is hidden when results are displayed
}

// CSRF Token function
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Update deduction information based on employment type
function updateDeductionInfo(employmentType) {
    const deductionCards = document.querySelectorAll('.deduction-card');

    deductionCards.forEach(card => {
        const cardTitle = card.querySelector('.card-title, h6')?.textContent || '';

        if (employmentType === 'CONTRACT') {
            if (cardTitle.includes('NSSF') || cardTitle.includes('Housing Levy')) {
                // Add exemption notice for contract employees
                card.style.opacity = '0.5';
                let exemptionNotice = card.querySelector('.exemption-notice');
                if (!exemptionNotice) {
                    exemptionNotice = document.createElement('div');
                    exemptionNotice.className = 'exemption-notice alert alert-info mt-2 mb-0';
                    exemptionNotice.innerHTML = '<small><i class="bi bi-info-circle me-1"></i>Exempt for contract employees</small>';
                    card.appendChild(exemptionNotice);
                }
            } else {
                // Remove exemption styling for SHIF and PAYE
                card.style.opacity = '1';
                const exemptionNotice = card.querySelector('.exemption-notice');
                if (exemptionNotice) {
                    exemptionNotice.remove();
                }
            }
        } else {
            // Remove exemption styling for all other employment types
            card.style.opacity = '1';
            const exemptionNotice = card.querySelector('.exemption-notice');
            if (exemptionNotice) {
                exemptionNotice.remove();
            }
        }
    });
}
