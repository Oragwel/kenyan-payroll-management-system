# 📡 API Documentation

## Overview

The Kenyan Payroll Management System provides a comprehensive API for programmatic access to payroll data and operations. This document covers all available endpoints, authentication, and usage examples.

## 🔐 Authentication

### API Token Authentication
```python
# Obtain API token
POST /api/auth/token/
{
    "username": "your_username",
    "password": "your_password"
}

# Response
{
    "token": "your_api_token_here",
    "expires_at": "2024-12-31T23:59:59Z"
}
```

### Using API Token
```bash
# Include token in headers
curl -H "Authorization: Token your_api_token_here" \
     -H "Content-Type: application/json" \
     https://your-domain.com/api/employees/
```

## 👥 Employee Management API

### List Employees
```http
GET /api/employees/
```

**Parameters:**
- `page` (int): Page number for pagination
- `page_size` (int): Number of results per page (max 100)
- `search` (string): Search by name, email, or payroll number
- `department` (int): Filter by department ID
- `employment_type` (string): Filter by employment type
- `is_active` (boolean): Filter by active status

**Response:**
```json
{
    "count": 150,
    "next": "https://your-domain.com/api/employees/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "payroll_number": "EMP001",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@company.com",
            "national_id": "12345678",
            "kra_pin": "A123456789P",
            "department": {
                "id": 1,
                "name": "Administration",
                "code": "ADMIN"
            },
            "job_title": {
                "id": 1,
                "title": "Manager"
            },
            "employment_type": "PERMANENT",
            "date_hired": "2023-01-15",
            "is_active": true,
            "created_at": "2023-01-15T10:30:00Z",
            "updated_at": "2023-01-15T10:30:00Z"
        }
    ]
}
```

### Get Employee Details
```http
GET /api/employees/{id}/
```

**Response:**
```json
{
    "id": 1,
    "payroll_number": "EMP001",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@company.com",
    "phone": "+254712345678",
    "national_id": "12345678",
    "kra_pin": "A123456789P",
    "nssf_number": "123456789",
    "shif_number": "987654321",
    "date_of_birth": "1990-05-15",
    "gender": "M",
    "marital_status": "SINGLE",
    "address": "123 Main Street, Nairobi",
    "department": {
        "id": 1,
        "name": "Administration",
        "code": "ADMIN",
        "description": "Administrative Department"
    },
    "job_title": {
        "id": 1,
        "title": "Manager",
        "description": "Department Manager"
    },
    "employment_type": "PERMANENT",
    "date_hired": "2023-01-15",
    "salary_structure": {
        "basic_salary": "50000.00",
        "house_allowance": "15000.00",
        "transport_allowance": "10000.00",
        "medical_allowance": "5000.00",
        "other_allowances": "0.00"
    },
    "banking_info": {
        "bank_name": "Equity Bank",
        "bank_code": "68058",
        "account_number": "1234567890",
        "branch": "Nairobi Branch"
    },
    "is_active": true,
    "created_at": "2023-01-15T10:30:00Z",
    "updated_at": "2023-01-15T10:30:00Z"
}
```

### Create Employee
```http
POST /api/employees/
```

**Request Body:**
```json
{
    "payroll_number": "EMP002",
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane.smith@company.com",
    "phone": "+254723456789",
    "national_id": "87654321",
    "kra_pin": "B987654321Q",
    "department_id": 1,
    "job_title_id": 2,
    "employment_type": "PERMANENT",
    "date_hired": "2023-02-01",
    "basic_salary": "45000.00",
    "house_allowance": "12000.00",
    "transport_allowance": "8000.00"
}
```

### Update Employee
```http
PUT /api/employees/{id}/
PATCH /api/employees/{id}/
```

### Delete Employee
```http
DELETE /api/employees/{id}/
```

## 💰 Payroll API

### Payroll Calculator
```http
POST /api/payroll/calculate/
```

**Request Body:**
```json
{
    "gross_salary": "80000.00",
    "employment_type": "PERMANENT",
    "has_nssf": true,
    "has_shif": true,
    "has_housing_levy": true,
    "insurance_premium": "2000.00",
    "pension_contribution": "1000.00"
}
```

**Response:**
```json
{
    "gross_salary": "80000.00",
    "taxable_income": "80000.00",
    "paye_tax": "11600.00",
    "personal_relief": "2400.00",
    "insurance_relief": "2000.00",
    "pension_relief": "1000.00",
    "net_paye": "6200.00",
    "nssf_employee": "2160.00",
    "nssf_employer": "2160.00",
    "shif_contribution": "2750.00",
    "housing_levy_employee": "1200.00",
    "housing_levy_employer": "1200.00",
    "total_deductions": "11310.00",
    "net_salary": "68690.00",
    "employer_cost": "83360.00"
}
```

### Generate Payroll
```http
POST /api/payroll/generate/
```

**Request Body:**
```json
{
    "period_year": 2024,
    "period_month": 3,
    "employee_ids": [1, 2, 3],
    "department_ids": [1, 2]
}
```

### Get Payroll Periods
```http
GET /api/payroll/periods/
```

**Response:**
```json
{
    "count": 12,
    "results": [
        {
            "id": 1,
            "year": 2024,
            "month": 3,
            "name": "March 2024",
            "start_date": "2024-03-01",
            "end_date": "2024-03-31",
            "status": "COMPLETED",
            "total_employees": 150,
            "gross_payroll": "12000000.00",
            "net_payroll": "9500000.00",
            "total_deductions": "2500000.00",
            "created_at": "2024-03-01T09:00:00Z"
        }
    ]
}
```

### Get Payslips
```http
GET /api/payroll/payslips/
```

**Parameters:**
- `period_id` (int): Filter by payroll period
- `employee_id` (int): Filter by employee
- `format` (string): Response format ('json', 'pdf')

## 🏢 Organization API

### Get Organizations
```http
GET /api/organizations/
```

### Get Departments
```http
GET /api/departments/
```

**Response:**
```json
{
    "count": 11,
    "results": [
        {
            "id": 1,
            "name": "Administration",
            "code": "ADMIN",
            "description": "Administrative Department",
            "organization": 1,
            "employee_count": 25,
            "is_active": true
        },
        {
            "id": 2,
            "name": "Finance",
            "code": "FIN",
            "description": "Finance and Accounting Department",
            "organization": 1,
            "employee_count": 15,
            "is_active": true
        }
    ]
}
```

### Get Job Titles
```http
GET /api/job-titles/
```

## 📊 Reports API

### Payroll Summary Report
```http
GET /api/reports/payroll-summary/
```

**Parameters:**
- `period_id` (int): Payroll period ID
- `format` (string): 'json', 'pdf', 'excel'

### Department Analysis
```http
GET /api/reports/department-analysis/
```

### Tax Report
```http
GET /api/reports/tax-report/
```

**Parameters:**
- `year` (int): Tax year
- `month` (int): Tax month (optional)
- `format` (string): 'json', 'pdf', 'excel'

## 🔍 Search API

### Global Search
```http
GET /api/search/
```

**Parameters:**
- `q` (string): Search query
- `type` (string): 'employees', 'departments', 'payslips'

## 📤 Bulk Operations API

### Bulk Employee Import
```http
POST /api/employees/bulk-import/
```

**Request (multipart/form-data):**
```
file: employee_data.xlsx
```

**Response:**
```json
{
    "success": true,
    "imported_count": 45,
    "error_count": 2,
    "errors": [
        {
            "row": 3,
            "field": "kra_pin",
            "message": "Invalid KRA PIN format"
        }
    ]
}
```

### Bulk Export
```http
POST /api/employees/bulk-export/
```

**Request Body:**
```json
{
    "employee_ids": [1, 2, 3],
    "format": "excel",
    "include_salary": false
}
```

## 🔒 Security API

### Audit Logs
```http
GET /api/audit-logs/
```

**Parameters:**
- `user_id` (int): Filter by user
- `action` (string): Filter by action type
- `start_date` (date): Filter from date
- `end_date` (date): Filter to date

### Security Events
```http
GET /api/security/events/
```

## 📋 Error Handling

### Standard Error Response
```json
{
    "error": true,
    "message": "Validation failed",
    "details": {
        "field_name": ["This field is required."],
        "another_field": ["Invalid format."]
    },
    "code": "VALIDATION_ERROR"
}
```

### HTTP Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `429` - Rate Limited
- `500` - Internal Server Error

## 🚀 Rate Limiting

### Default Limits
- **Authenticated Users**: 1000 requests/hour
- **Anonymous Users**: 100 requests/hour
- **Bulk Operations**: 10 requests/hour

### Rate Limit Headers
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## 📝 Usage Examples

### Python Example
```python
import requests

# Authentication
auth_response = requests.post('https://your-domain.com/api/auth/token/', {
    'username': 'your_username',
    'password': 'your_password'
})
token = auth_response.json()['token']

# Headers for authenticated requests
headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json'
}

# Get employees
employees = requests.get('https://your-domain.com/api/employees/', headers=headers)
print(employees.json())

# Calculate payroll
calculation = requests.post('https://your-domain.com/api/payroll/calculate/', 
    headers=headers,
    json={
        'gross_salary': '50000.00',
        'employment_type': 'PERMANENT'
    }
)
print(calculation.json())
```

### JavaScript Example
```javascript
// Authentication
const authResponse = await fetch('https://your-domain.com/api/auth/token/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        username: 'your_username',
        password: 'your_password'
    })
});
const { token } = await authResponse.json();

// Get employees
const employeesResponse = await fetch('https://your-domain.com/api/employees/', {
    headers: { 'Authorization': `Token ${token}` }
});
const employees = await employeesResponse.json();
console.log(employees);
```

This API documentation provides comprehensive access to all payroll system functionality through RESTful endpoints with proper authentication and error handling.
