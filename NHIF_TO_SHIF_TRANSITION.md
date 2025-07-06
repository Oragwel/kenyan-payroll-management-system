# NHIF to SHIF Transition in Kenya

## Overview

This payroll management system has been updated to reflect Kenya's transition from NHIF (National Hospital Insurance Fund) to SHIF (Social Health Insurance Fund) as part of the Universal Health Coverage (UHC) reforms.

## Key Changes

### What Changed
- **NHIF Removed**: The old NHIF contribution system with fixed salary bands has been completely removed
- **SHIF Implemented**: The new SHIF system with percentage-based contributions is now active

### NHIF vs SHIF Comparison

| Aspect | NHIF (Old System) | SHIF (New System) |
|--------|-------------------|-------------------|
| **Contribution Method** | Fixed amounts based on salary bands | Percentage-based (2.75% of gross salary) |
| **Minimum Contribution** | KES 150 (for lowest band) | KES 300 |
| **Maximum Contribution** | KES 1,700 (for highest band) | No maximum (2.75% of any salary) |
| **Salary Bands** | 17 different bands | No bands - single percentage |
| **Coverage** | Limited coverage | Universal Health Coverage |

### Examples of Contribution Changes

| Monthly Salary | NHIF (Old) | SHIF (New) | Difference |
|----------------|------------|------------|------------|
| KES 25,000 | KES 850 | KES 687.50 | -KES 162.50 |
| KES 50,000 | KES 1,200 | KES 1,375 | +KES 175 |
| KES 80,000 | KES 1,500 | KES 2,200 | +KES 700 |
| KES 120,000 | KES 1,700 | KES 3,300 | +KES 1,600 |
| KES 200,000 | KES 1,700 | KES 5,500 | +KES 3,800 |

## Implementation Details

### Database Changes
- Removed `NHIFRate` model from `statutory_deductions` app
- Removed `nhif_contribution` field from `Payslip` model
- Removed `total_nhif` field from `PayrollSummary` model
- Kept `SHIFRate` model with enhanced documentation

### Code Changes
- Removed `NHIFCalculator` class
- Enhanced `SHIFCalculator` with detailed documentation
- Updated all payroll calculations to use SHIF instead of NHIF
- Updated test cases to reflect SHIF-only calculations

### Benefits of SHIF
1. **Simplified Calculation**: Single percentage rate instead of complex bands
2. **Progressive Contributions**: Higher earners contribute more (fairer system)
3. **Universal Coverage**: Better healthcare access for all Kenyans
4. **Transparency**: Clear percentage-based system

### Migration Notes
- All existing NHIF data has been removed from the system
- SHIF rates are set at 2.75% with a minimum of KES 300
- The system automatically calculates SHIF contributions for all employees
- No manual intervention required for payroll processing

## Usage

The payroll system now automatically:
1. Calculates SHIF at 2.75% of gross salary
2. Applies minimum contribution of KES 300 where applicable
3. Includes SHIF in total statutory deductions
4. Generates payslips with SHIF instead of NHIF

## Future Updates

The SHIF rates and minimum contributions can be updated through:
1. Django admin interface
2. Management commands
3. Database updates to the `SHIFRate` model

This ensures the system remains compliant with any future changes to SHIF regulations.
