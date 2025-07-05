# 🇰🇪 Kenyan Payroll Management System

A comprehensive, Django-based payroll management system designed specifically for Kenyan employment structure and statutory compliance requirements. This system supports government entities, private companies, parastatals, NGOs, and other organizations operating in Kenya.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2%2B-green.svg)](https://djangoproject.com)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Mobile](https://img.shields.io/badge/Mobile-Responsive-orange.svg)](#responsive-design)
[![Security](https://img.shields.io/badge/Security-Enhanced-red.svg)](#security-features)
[![Vercel](https://img.shields.io/badge/Deploy-Vercel-black.svg)](https://vercel.com)
[![Status](https://img.shields.io/badge/Status-In%20Development-yellow.svg)](#development-status)

## 🌟 Key Features Overview

### 💼 Core Payroll Management
- **🧑‍💼 Employee Management**: Complete employee lifecycle with Kenyan-specific fields (National ID, KRA PIN, SHIF, NSSF)
- **💰 Payroll Processing**: Automated salary calculations with statutory deductions and tax relief
- **📄 Payslip Generation**: Professional payslips with thermal printing support (80mm width, A5+ length)
- **📊 Bulk Operations**: Excel-based mass employee import/export with validation and templates
- **🏢 Multi-Organization Support**: Manage multiple entities with individual branding and settings
- **🔄 Payroll Periods**: Monthly payroll cycles with historical data and period management

### 🇰🇪 Kenyan Statutory Compliance
- **💸 PAYE Tax Calculation**: Automated Pay As You Earn tax calculations per KRA guidelines with tax reliefs
- **🛡️ NSSF Contributions**: National Social Security Fund calculations (Tier I & II) for eligible employees
- **🏥 SHIF Integration**: Social Health Insurance Fund (replacing NHIF) with updated contribution rates
- **🏠 Housing Levy**: Affordable Housing Levy calculations (1.5% mandatory for all employees)
- **📋 Employment Types**: Support for Permanent, Contract, Casual Worker, and Intern classifications
- **✅ Data Validation**: KRA PIN, National ID, SHIF, and NSSF number format validation

### 🎨 User Experience & Design
- **📱 Mobile Responsive**: Fully responsive design optimized for phones, tablets, and Kindles
- **🎯 Adaptive UI**: Table-to-card transformation on mobile devices for better usability
- **🏷️ Organization Branding**: Logo integration throughout system (dashboard, reports, payslips)
- **🔍 Smart Search**: Auto-filtering search with department, employment type, and status filters
- **📈 Data Visualization**: Beautiful charts and enhanced data visualization for reports
- **🎨 Professional Design**: Modern Bootstrap 5 interface with Kenyan color scheme

### 🔒 Security & Access Control
- **🛡️ Enhanced Security**: Password saving restrictions, secure login, and session management
- **🔐 Role-Based Access**: Admin, HR, and employee access levels with granular permissions
- **🔗 Secure URLs**: Obfuscated URLs with token-based access control and audit logging
- **📊 Activity Monitoring**: Comprehensive audit trails and security event logging
- **🚫 Access Restrictions**: Protected routes with authentication requirements
- **🔒 Data Protection**: Compliance with Kenyan Data Protection Act requirements

### 📊 Reporting & Analytics
- **📈 Dashboard Analytics**: Real-time statistics and departmental analysis
- **📋 Comprehensive Reports**: Payroll summaries, tax reports, and statutory returns
- **📄 Export Options**: PDF and Excel exports with landscape orientation and organization branding
- **📊 Department Analysis**: Payroll breakdown by department with visual charts
- **💹 Financial Summaries**: Gross payroll, net payroll, and statutory deduction totals
- **📅 Historical Data**: Period-based reporting with trend analysis

## 🏗️ System Architecture

### 📁 Project Structure
```
kenyan-payroll-system/
├── payroll/                    # Main Django project configuration
│   ├── settings.py            # Django settings with security configurations
│   ├── urls.py                # Main URL routing with secure patterns
│   └── wsgi.py                # WSGI configuration for deployment
├── employees/                  # Employee and organization management
│   ├── models.py              # Employee, Organization, Department, JobTitle models
│   ├── views.py               # Employee CRUD operations and bulk import
│   ├── forms.py               # Employee forms with Kenyan field validation
│   ├── admin.py               # Django admin customizations
│   └── management/commands/   # Custom management commands
├── payroll_processing/         # Payroll calculations and processing
│   ├── models.py              # PayrollPeriod, Payslip models
│   ├── views.py               # Payroll generation and calculator views
│   ├── calculators/           # Statutory deduction calculators
│   │   ├── paye_calculator.py # PAYE tax calculations with reliefs
│   │   ├── nssf_calculator.py # NSSF Tier I & II calculations
│   │   ├── shif_calculator.py # SHIF contribution calculations
│   │   └── housing_calculator.py # Housing Levy calculations
│   └── utils/                 # Payroll utilities and helpers
├── core/                       # Security and core functionality
│   ├── views.py               # Dashboard, login, and security views
│   ├── admin_views.py         # Admin-specific views and reports
│   ├── security.py            # URL obfuscation and token management
│   └── middleware.py          # Custom security middleware
├── templates/                  # HTML templates (mobile-responsive)
│   ├── base/                  # Base templates with responsive navigation
│   ├── employees/             # Employee management templates
│   │   ├── employee_list.html # Responsive table/card view
│   │   ├── employee_form.html # Mobile-optimized forms
│   │   └── partials/          # Reusable template components
│   ├── payroll/               # Payroll processing templates
│   ├── registration/          # Authentication templates with security
│   └── dashboard.html         # Mobile-responsive dashboard
├── static/                     # Static assets
│   ├── css/
│   │   └── custom.css         # Comprehensive responsive CSS
│   ├── js/                    # JavaScript for interactivity
│   └── images/                # System images and icons
├── media/                      # User uploads
│   ├── logos/                 # Organization logos
│   └── documents/             # Generated reports and documents
├── docs/                       # Technical documentation
│   ├── SECURITY.md            # Security implementation guide
│   ├── DEPLOYMENT.md          # Deployment instructions
│   ├── API.md                 # API documentation
│   └── CHANGELOG.md           # Version history and updates
├── requirements.txt            # Python dependencies
├── manage.py                  # Django management script
└── README.md                  # This file
```

### 🗄️ Database Models

#### **Core Models**
- **Organization**: Multi-entity support with branding, contact info, and statutory numbers
- **Employee**: Comprehensive employee data with Kenyan-specific fields
- **Department**: Organizational departments (Administration, Finance, HR, ICT, Municipality, etc.)
- **JobTitle**: Job positions with salary structures
- **SalaryStructure**: Employee compensation details and allowances

#### **Payroll Models**
- **PayrollPeriod**: Monthly/periodic payroll cycles with status tracking
- **Payslip**: Individual employee pay records with statutory breakdowns
- **PayrollSummary**: Aggregated payroll data for reporting

#### **Security Models**
- **AuditLog**: Comprehensive activity tracking and security monitoring
- **SecureToken**: URL obfuscation and access control tokens
- **UserSession**: Enhanced session management and tracking

## 🎯 Detailed Features

### 👥 Employee Management
- **📝 Employee Registration**: Comprehensive employee onboarding with Kenyan-specific fields
- **🆔 National ID Integration**: 8-digit National ID validation and management
- **📋 Employment Types**: Support for Permanent, Contract, Casual Worker, and Intern classifications
- **🏢 Department Management**: 11 default departments including Municipality, Ugatuzi, and standard government departments
- **💼 Job Title Management**: Flexible job title system with salary structure integration
- **📊 Bulk Import/Export**: Excel-based mass operations with validation and error reporting
- **🔍 Advanced Search**: Auto-filtering search by name, department, employment type, and status
- **📱 Mobile Employee Cards**: Responsive card view for mobile devices with essential information

### 💰 Payroll Processing
- **🧮 Automated Calculations**: Real-time payroll calculations with statutory deductions
- **📅 Payroll Periods**: Monthly payroll cycles with historical data and period management
- **🚫 Future Period Restriction**: Prevents advance payroll processing for security
- **👨‍💼 Admin-Only Generation**: Restricted payroll generation to authorized administrators
- **📄 Professional Payslips**: A4 web view with 80mm thermal printing optimization
- **📊 Bulk Payslip Generation**: Mass payslip creation with PDF and Excel export options
- **💹 Real-time Calculator**: Interactive payroll calculator with instant results
- **📈 Department Analytics**: Payroll breakdown and analysis by department

### 🇰🇪 Kenyan Statutory Compliance
- **💸 PAYE Tax System**:
  - Progressive tax rates per KRA guidelines
  - Personal relief (KES 2,400/month)
  - Insurance relief (up to KES 5,000/month)
  - Mortgage interest relief
  - Pension contribution relief
  - Post-retirement medical fund relief
- **🛡️ NSSF Contributions**:
  - Tier I: 6% on first KES 7,000 (max KES 420)
  - Tier II: 6% on next KES 29,000 (max KES 1,740)
  - Employer matching contributions
  - Contract employee exemptions
- **🏥 SHIF Integration**:
  - Updated contribution rates replacing NHIF
  - Universal coverage for all employee types
  - Automated deduction calculations
- **🏠 Housing Levy**:
  - 1.5% mandatory contribution for all employees
  - Employer matching (1.5%)
  - Contract employee exemptions available

### 🔒 Security Features
- **🛡️ Enhanced Login Security**:
  - Password saving restrictions across all browsers
  - Multi-layer password manager prevention
  - Secure session management
  - Auto-logout on inactivity
- **🔗 URL Security**:
  - Obfuscated URLs with token-based access
  - Route protection and authentication requirements
  - Audit logging for all access attempts
  - Security monitoring and alerts
- **👤 Role-Based Access Control**:
  - Admin: Full system access and user management
  - HR: Employee management and payroll viewing
  - Employee: Personal information and payslip access
  - Granular permission system

### 📱 Responsive Design
- **📱 Mobile-First Approach**: Designed for mobile devices with progressive enhancement
- **💻 Cross-Device Compatibility**: Optimized for phones, tablets, Kindles, and desktops
- **🔄 Adaptive UI Components**:
  - Tables transform to cards on mobile
  - Responsive navigation with collapsible menu
  - Touch-friendly buttons and form elements
  - Optimized typography and spacing
- **🎨 Professional Branding**:
  - Organization logo integration throughout system
  - Consistent branding in reports and payslips
  - Kenyan color scheme and professional design
  - Print-optimized layouts

### 📊 Reporting & Analytics
- **📈 Dashboard Analytics**:
  - Real-time employee statistics
  - Department-wise payroll breakdown
  - Visual charts and graphs
  - Key performance indicators
- **📋 Comprehensive Reports**:
  - Payroll summary reports
  - Tax and statutory returns
  - Department analysis
  - Employee listings with filters
- **📄 Export Capabilities**:
  - PDF exports with organization branding
  - Excel exports with landscape orientation
  - Bulk payslip downloads
  - Print-optimized formats

## 🚀 Quick Start

### 📋 Prerequisites
- **Python**: 3.8+ (recommended: 3.10+)
- **Django**: 4.2+ (included in requirements)
- **Database**: SQLite (default) or PostgreSQL/MySQL for production
- **Browser**: Modern web browser with JavaScript enabled
- **OS**: Windows, macOS, or Linux

### 🛠️ Installation

1. **📥 Clone the repository**
   ```bash
   git clone <repository-url>
   cd kenyan-payroll-system
   ```

2. **🐍 Create virtual environment**
   ```bash
   python -m venv .venv

   # On Linux/macOS:
   source .venv/bin/activate

   # On Windows:
   .venv\Scripts\activate
   ```

3. **📦 Install dependencies**
   ```bash
   # Install from requirements file (recommended)
   pip install -r requirements.txt

   # Or install manually:
   pip install django==4.2.7
   pip install reportlab==4.0.4
   pip install xlsxwriter==3.1.9
   pip install pandas==2.1.3
   pip install pillow==10.1.0
   pip install openpyxl==3.1.2
   ```

4. **🗄️ Database setup**
   ```bash
   # Create and apply migrations
   python manage.py makemigrations
   python manage.py migrate

   # Load initial data (optional)
   python manage.py loaddata initial_data.json
   ```

5. **👤 Create superuser**
   ```bash
   python manage.py createsuperuser
   # Follow prompts to create admin account
   ```

6. **🚀 Run development server**
   ```bash
   python manage.py runserver

   # Server will start at: http://127.0.0.1:8000/
   # Admin interface: http://127.0.0.1:8000/admin/
   ```

### 🎯 Initial Setup

1. **🏢 Configure Organization**
   - Login with superuser account
   - Navigate to Admin → Organizations
   - Add your organization details and logo

2. **🏗️ Setup Departments**
   - Default departments are auto-created
   - Add custom departments as needed
   - Configure department codes and descriptions

3. **👥 Add Employees**
   - Use bulk import for multiple employees
   - Download Excel template from Employee → Bulk Import
   - Or add employees individually through the interface

4. **💰 Configure Payroll**
   - Set up salary structures
   - Configure statutory rates if needed
   - Create first payroll period

## 📖 Usage Guide

### 🏢 Organization Management

1. **Setup Organization Profile**
   ```
   Admin Dashboard → Organizations → Add Organization
   - Organization Type: Government/Private/NGO/Parastatal
   - Name: Full organization name
   - Logo: Upload organization logo (recommended: 200x200px)
   - Contact Details: Address, phone, email
   - Statutory Numbers: KRA PIN, NSSF Employer Number, SHIF Number
   ```

2. **Configure Branding**
   - Logo appears on dashboard, reports, and payslips
   - Organization details included in all exports
   - Professional document formatting

### 👥 Employee Management

1. **Individual Employee Addition**
   ```
   Employees → Add New Employee
   - Personal Information: Name, National ID, Date of Birth
   - Employment Details: Department, Job Title, Employment Type
   - Contact Information: Email, Phone, Address
   - Statutory Information: KRA PIN, NSSF Number, SHIF Number
   - Banking Information: Bank Code, Account Number, Branch
   ```

2. **Bulk Employee Import**
   ```
   Employees → Bulk Import → Download Template
   - Fill Excel template with employee data
   - Upload completed file
   - Review validation results
   - Confirm import
   ```

3. **Employee Search & Filtering**
   ```
   Employees → Search
   - Text Search: Name, payroll number, email, KRA PIN
   - Department Filter: Select specific department
   - Employment Type: Permanent, Contract, Casual, Intern
   - Status: Active/Inactive employees
   ```

### 💰 Payroll Processing

1. **Payroll Calculator**
   ```
   Payroll → Calculator
   - Enter gross salary
   - Select employment type
   - View real-time calculations:
     * PAYE tax with reliefs
     * NSSF contributions (Tier I & II)
     * SHIF contributions
     * Housing Levy
     * Net pay calculation
   ```

2. **Generate Payroll**
   ```
   Payroll → Generate Payroll (Admin Only)
   - Select payroll period (current/past months only)
   - Choose employees or departments
   - Review calculations
   - Generate payslips
   - Export reports (PDF/Excel)
   ```

3. **Payroll Periods Management**
   ```
   Payroll → Payroll Periods (Admin Only)
   - Create new periods
   - View historical payrolls
   - Delete periods (bulk/individual)
   - Export period summaries
   ```

### 📊 Reports & Analytics

1. **Dashboard Analytics**
   ```
   Dashboard → Statistics
   - Total/Active employees
   - Department breakdown
   - Payroll summaries
   - Visual charts and graphs
   ```

2. **Export Reports**
   ```
   Reports → Export Options
   - Payroll Summary (PDF/Excel)
   - Tax Reports (KRA compliance)
   - Statutory Returns (NSSF, SHIF, Housing Levy)
   - Employee Lists (filtered)
   - Department Analysis
   ```

### 🔒 Security Features

1. **User Access Control**
   ```
   Admin → Users → Create User
   - Assign roles (Admin/HR/Employee)
   - Set permissions
   - Configure access levels
   ```

2. **Secure Login**
   ```
   Login Security Features:
   - Password saving disabled
   - Session timeout
   - Audit logging
   - Failed login monitoring
   ```

## 🇰🇪 Kenyan Compliance

### Statutory Rates (2024)
- **PAYE Tax**: Progressive rates with KES 2,400 personal relief
- **NSSF**: 6% employee + 6% employer (Tier I: KES 7,000, Tier II: KES 29,000)
- **SHIF**: Updated rates replacing NHIF
- **Housing Levy**: 1.5% employee + 1.5% employer

### Employment Type Compliance
- **Permanent Employees**: All statutory deductions apply
- **Contract Employees**: SHIF only (NSSF and Housing Levy exempt)
- **Casual Workers**: SHIF + Housing Levy (NSSF not mandatory)
- **Interns**: All standard deductions apply

## 👥 User Management

### Access Levels

1. **Super Admin**
   - Full system access
   - User management
   - Organization configuration
   - System settings

2. **Admin/HR Staff**
   - Employee management
   - Payroll processing
   - Report generation
   - Bulk operations

3. **Employees**
   - View personal payslips
   - Access personal information
   - Download pay documents

### Security Features

- **Authentication Required**: All routes protected
- **URL Obfuscation**: Sensitive URLs are obfuscated
- **Token-Based Access**: Secure payslip access
- **Audit Logging**: All actions logged
- **Session Management**: Secure session handling

## 💼 Payroll Processing

### Monthly Payroll Workflow

1. **Generate Payroll**
   - Select payroll period (month/year)
   - System validates no future periods
   - Automatic employee inclusion

2. **Review Calculations**
   - Verify salary calculations
   - Check statutory deductions
   - Review gross and net pay

3. **Process Payroll**
   - Generate all payslips
   - Create payroll summary
   - Export reports

4. **Distribution**
   - Download individual payslips
   - Bulk download (PDF/Excel)
   - Print thermal payslips (80mm)

### Salary Calculations

```
Gross Salary = Basic Salary + Allowances
Taxable Income = Gross Salary - NSSF Contribution
PAYE = Tax on Taxable Income
SHIF = Based on gross salary
Housing Levy = 1.5% of gross salary
Net Pay = Gross Salary - (PAYE + NSSF + SHIF + Housing Levy + Other Deductions)
```

## 📊 Reports & Analytics

### Available Reports
- **Payroll Summary**: Monthly payroll totals
- **Tax Reports**: PAYE analysis and KRA returns
- **Statutory Returns**: NSSF, SHIF, Housing Levy reports
- **Employee Lists**: Comprehensive employee data
- **Department Analysis**: Departmental payroll breakdown

### Export Formats
- **PDF**: Professional formatted reports with organization branding
- **Excel**: Detailed spreadsheets for analysis
- **Thermal Printing**: 80mm payslips for receipt printers

## 🔧 Customization

### Organization Branding
- Upload organization logo (recommended: 200x80px)
- Customize organization details
- Set default organization for multi-entity setups

### Statutory Rates
- Update tax bands in `statutory_deductions/utils.py`
- Modify NSSF rates as per government changes
- Adjust SHIF rates when updated
- Configure Housing Levy percentages

### Templates
- Customize payslip layouts in `templates/payroll/`
- Modify email templates
- Update report formats

## 🛡️ Security Implementation

### URL Security
- Obfuscated sensitive URLs
- Token-based payslip access
- CSRF protection on all forms
- Secure session management

### Data Protection
- Input validation and sanitization
- SQL injection prevention
- XSS protection
- Secure file uploads

### Audit Trail
- User action logging
- Payroll processing logs
- Security event monitoring
- Access attempt tracking

## 📱 Mobile Support

### Responsive Design
- Bootstrap 5 responsive framework
- Mobile-optimized forms
- Touch-friendly interfaces
- Adaptive layouts

### Mobile Features
- Mobile payslip viewing
- Responsive tables
- Touch-optimized navigation
- Mobile-friendly reports

## 🔄 Data Management

### Backup & Recovery
- Regular database backups recommended
- Media files backup (logos, documents)
- Export functionality for data portability

### Data Import/Export
- **Employee Import**: Excel template-based bulk import
- **Data Export**: Multiple format support
- **Report Generation**: Automated report creation
- **Payslip Archives**: Historical payslip storage

## 🚨 Troubleshooting

### Common Issues

1. **Migration Errors**
   ```bash
   python manage.py makemigrations --empty employees
   python manage.py migrate --fake-initial
   ```

2. **Static Files Not Loading**
   ```bash
   python manage.py collectstatic
   ```

3. **Permission Errors**
   - Ensure proper file permissions
   - Check media directory access
   - Verify database permissions

### Support Resources
- Check existing documentation files:
  - `KENYAN_STATUTORY_COMPLIANCE.md`
  - `SECURITY_IMPLEMENTATION.md`
  - `PAYSLIP_PRINTING_GUIDE.md`
  - `NHIF_TO_SHIF_TRANSITION.md`

## 📄 License

This project is developed for Kenyan organizations and complies with local employment and tax regulations. Please ensure compliance with current statutory requirements.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Implement changes
4. Test thoroughly
5. Submit pull request

## 📞 Support

For technical support or customization requests, please refer to the documentation files or contact the development team.

## 🎯 Use Cases

### Government Entities
- **County Governments**: Complete payroll management for county staff
- **National Government**: Ministry and department payroll processing
- **Parastatals**: State corporation employee management
- **Public Universities**: Academic and administrative staff payroll

### Private Sector
- **SMEs**: Small and medium enterprise payroll
- **Corporations**: Large company multi-department payroll
- **NGOs**: Non-profit organization staff management
- **International Organizations**: UN agencies, embassies, etc.

### Key Benefits
- **Compliance Assurance**: Always up-to-date with Kenyan regulations
- **Cost Effective**: Reduce payroll processing costs
- **Time Saving**: Automated calculations and bulk operations
- **Accuracy**: Eliminate manual calculation errors
- **Professional**: Branded payslips and reports

## 📈 Performance & Scalability

### System Capacity
- **Employees**: Supports 1000+ employees per organization
- **Organizations**: Multi-tenant architecture
- **Concurrent Users**: Optimized for multiple simultaneous users
- **Data Storage**: Efficient database design for large datasets

### Performance Features
- **Bulk Processing**: Handle hundreds of employees simultaneously
- **Optimized Queries**: Fast database operations
- **Caching**: Improved response times
- **Pagination**: Efficient large dataset handling

## 🔍 Testing & Quality Assurance

### Test Coverage
- **Unit Tests**: Core calculation functions
- **Integration Tests**: End-to-end payroll processing
- **Validation Tests**: Statutory compliance verification
- **Security Tests**: Authentication and authorization

### Quality Features
- **Input Validation**: Comprehensive data validation
- **Error Handling**: Graceful error management
- **Data Integrity**: Referential integrity constraints
- **Audit Trail**: Complete action logging

## 🌐 Deployment Options

### Development Environment
```bash
# Quick development setup
python manage.py runserver
# Access at http://127.0.0.1:8000
```

### Production Deployment
```bash
# Production settings
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']

# Database configuration
# Use PostgreSQL or MySQL for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'payroll_db',
        'USER': 'payroll_user',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Static files
python manage.py collectstatic
```

### Docker Deployment
```dockerfile
# Example Dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 📋 API Documentation

### Core Endpoints
- **Employee Management**: CRUD operations for employees
- **Payroll Processing**: Payroll generation and management
- **Reports**: Data export and reporting endpoints
- **Authentication**: User management and security

### Example API Usage
```python
# Employee creation
POST /employees/create/
{
    "first_name": "John",
    "last_name": "Doe",
    "national_id": "12345678",
    "department": "Finance",
    "basic_salary": 50000
}

# Payroll generation
POST /payroll/generate/
{
    "period_month": 12,
    "period_year": 2024,
    "employees": ["all"]
}
```

## 🔧 Advanced Configuration

### Custom Statutory Rates
```python
# In statutory_deductions/utils.py
PAYE_BANDS = [
    (24000, 0.10),    # 10% for income up to 24,000
    (8333, 0.25),     # 25% for next 8,333
    (467667, 0.30),   # 30% for next 467,667
    (float('inf'), 0.35)  # 35% for income above 500,000
]

NSSF_RATE = 0.06  # 6% of pensionable pay
HOUSING_LEVY_RATE = 0.015  # 1.5% of gross salary
```

### Email Configuration
```python
# Email settings for payslip distribution
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Backup Configuration
```bash
# Database backup
python manage.py dumpdata > backup.json

# Media files backup
tar -czf media_backup.tar.gz media/

# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
python manage.py dumpdata > backups/db_backup_$DATE.json
tar -czf backups/media_backup_$DATE.tar.gz media/
```

## 📚 Documentation

### 📖 System Documentation
- **[🚀 Deployment Guide](docs/DEPLOYMENT.md)**: Production deployment instructions
- **[🔒 Security Implementation](docs/SECURITY.md)**: Comprehensive security features and best practices
- **[📡 API Documentation](docs/API.md)**: Complete RESTful API reference
- **[📋 Changelog](docs/CHANGELOG.md)**: Version history and feature updates
- **[🛠️ Installation Guide](#-installation)**: Development setup instructions (above)
- **[📖 Usage Guide](#-usage-guide)**: Complete user guide (above)

### 🔗 External Resources
- **[KRA Tax Guidelines](https://www.kra.go.ke)**: Official PAYE tax information and rates
- **[NSSF Rates](https://www.nssf.or.ke)**: Current contribution rates and regulations
- **[SHIF Information](https://www.sha.go.ke)**: Social Health Insurance Fund details
- **[Labour Laws](http://www.labour.go.ke)**: Kenyan employment regulations and compliance
- **[Housing Levy](https://www.housingfund.go.ke)**: Affordable Housing Levy information

## 🚀 Roadmap & Future Development

### 🎯 Version 2.1.0 (Q2 2024)
- **📡 RESTful API**: Complete API for third-party integrations
- **🔗 Bank Integration**: Direct bank file generation for salary transfers
- **📊 Advanced Analytics**: Business intelligence dashboards with KPIs
- **📱 PWA Support**: Progressive Web App for offline functionality
- **🔔 Notification System**: Email and SMS notifications for payroll events

### 🎯 Version 2.2.0 (Q3 2024)
- **🌍 Multi-Language**: Swahili language support and localization
- **🏦 KRA iTax Integration**: Direct tax filing and compliance reporting
- **📈 Predictive Analytics**: Payroll forecasting and budget planning
- **🔐 Advanced Security**: Two-factor authentication and SSO integration
- **📱 Mobile App**: Native iOS and Android applications

### 🎯 Version 3.0.0 (Q4 2024)
- **☁️ Cloud Deployment**: SaaS offering with multi-tenancy
- **🤖 AI Integration**: Automated payroll anomaly detection
- **🔗 ERP Integration**: SAP, Oracle, and other ERP system connectors
- **📊 Real-time Dashboards**: Live payroll monitoring and alerts
- **🌐 Multi-Currency**: Support for international organizations

### 🔮 Long-term Vision
- **🏢 Enterprise Features**: Advanced workflow management and approvals
- **📱 Biometric Integration**: Fingerprint and facial recognition for attendance
- **🤝 Government Integration**: Direct integration with government systems
- **🌍 Regional Expansion**: Support for other East African countries
- **🔬 Machine Learning**: Intelligent payroll optimization and insights

## 🤝 Contributing

### 🛠️ Development Setup
```bash
# Fork the repository
git clone https://github.com/your-username/kenyan-payroll-system.git
cd kenyan-payroll-system

# Create development branch
git checkout -b feature/your-feature-name

# Set up development environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run tests
python manage.py test

# Make your changes and commit
git add .
git commit -m "Add your feature description"
git push origin feature/your-feature-name
```

### 📋 Contribution Guidelines
- **Code Style**: Follow PEP 8 for Python code
- **Testing**: Write tests for new features
- **Documentation**: Update documentation for changes
- **Security**: Follow security best practices
- **Compliance**: Ensure Kenyan statutory compliance

### 🐛 Bug Reports
When reporting bugs, please include:
- **Environment**: OS, Python version, Django version
- **Steps to Reproduce**: Clear reproduction steps
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Screenshots**: If applicable

### 💡 Feature Requests
For new features, please provide:
- **Use Case**: Why is this feature needed?
- **Proposed Solution**: How should it work?
- **Alternatives**: Other solutions considered
- **Compliance**: Any regulatory requirements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 📋 License Summary
- ✅ **Commercial Use**: Use in commercial projects
- ✅ **Modification**: Modify the source code
- ✅ **Distribution**: Distribute the software
- ✅ **Private Use**: Use for private projects
- ❌ **Liability**: No warranty or liability
- ❌ **Trademark Use**: No trademark rights granted

## 🙏 Acknowledgments

### 🏛️ Government Agencies
- **Kenya Revenue Authority (KRA)**: Tax calculation guidelines and compliance requirements
- **National Social Security Fund (NSSF)**: Contribution rates and regulatory framework
- **Social Health Insurance Fund (SHIF)**: Health insurance contribution structures
- **Ministry of Labour**: Employment law guidance and compliance standards

### 🤝 Community Contributors
- **Beta Testers**: Early adopters who provided valuable feedback
- **Security Researchers**: Identified and helped fix security vulnerabilities
- **Compliance Experts**: Ensured adherence to Kenyan regulations
- **UI/UX Designers**: Improved user experience and mobile responsiveness

### 🛠️ Technology Stack
- **Django Framework**: Robust web framework for rapid development
- **Bootstrap**: Responsive UI framework for mobile-first design
- **PostgreSQL**: Reliable database for production deployments
- **ReportLab**: PDF generation for payslips and reports
- **Pandas**: Data analysis and Excel export functionality

## 📞 Support & Contact

### 🆘 Getting Help
- **📖 Documentation**: Check the comprehensive documentation in the `docs/` folder
- **🐛 Issues**: Report bugs and request features via [GitHub Issues](https://github.com/your-repo/issues)
- **💬 Discussions**: Join community discussions for general questions
- **📧 Email**: Contact support@your-domain.com for urgent issues

### 🏢 Professional Services
- **🎓 Training**: On-site training for organizations
- **🔧 Custom Development**: Tailored features and integrations
- **☁️ Hosting**: Managed hosting and maintenance services
- **📊 Consulting**: Payroll process optimization and compliance consulting

### 🌍 Community
- **👥 User Forum**: Share experiences and best practices
- **📚 Knowledge Base**: Searchable documentation and FAQs
- **🎥 Video Tutorials**: Step-by-step video guides
- **📱 Social Media**: Follow us for updates and announcements

---

## 🇰🇪 Built for Kenya

**Compliant with KRA, NSSF, SHIF & Housing Levy Requirements**

*This system is designed specifically for Kenyan organizations, ensuring full compliance with all statutory requirements including PAYE tax calculations, NSSF contributions, SHIF deductions, and Housing Levy. Regular updates maintain compliance with evolving regulations.*

### 🏆 Key Compliance Features
- ✅ **KRA PAYE**: Progressive tax rates with all reliefs
- ✅ **NSSF**: Tier I & II contributions with employer matching
- ✅ **SHIF**: Updated health insurance contributions
- ✅ **Housing Levy**: 1.5% employee + employer contributions
- ✅ **Employment Types**: Proper handling of all Kenyan employment classifications
- ✅ **Data Protection**: Compliant with Kenyan Data Protection Act

### 📊 System Statistics
- **🏢 Organizations Supported**: Government, Private, NGO, Parastatal
- **👥 Employee Capacity**: Unlimited employees per organization
- **📱 Device Support**: Desktop, Tablet, Mobile, Kindle
- **🔒 Security Level**: Enterprise-grade with comprehensive audit trails
- **📈 Uptime**: 99.9% availability with proper deployment
- **🌍 Localization**: Kenyan timezone, currency, and regulations

**Version 2.0.0** | **Last Updated**: January 2024 | **Next Update**: March 2024
