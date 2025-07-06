#!/bin/bash

# Kenyan Payroll Management System - Installation Script
# This script automates the setup process for the payroll system

echo "🇰🇪 Kenyan Payroll Management System - Installation Script"
echo "=========================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

echo "✅ pip3 found: $(pip3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if Django is installed correctly
echo "🔍 Verifying Django installation..."
python -c "import django; print(f'✅ Django {django.get_version()} installed successfully')"

# Run migrations
echo "🗄️ Setting up database..."
python manage.py makemigrations
python manage.py migrate

# Create media directories
echo "📁 Creating media directories..."
mkdir -p media/company_logos
mkdir -p media/payslips
mkdir -p media/reports

# Set permissions for media directories
chmod 755 media
chmod 755 media/company_logos
chmod 755 media/payslips
chmod 755 media/reports

# Collect static files
echo "📋 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser prompt
echo ""
echo "👤 Create a superuser account for system administration:"
echo "   This account will have full access to the payroll system."
echo ""
read -p "Do you want to create a superuser now? (y/n): " create_superuser

if [[ $create_superuser =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
else
    echo "⚠️ You can create a superuser later by running: python manage.py createsuperuser"
fi

# Installation complete
echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "📋 Next Steps:"
echo "1. Start the development server:"
echo "   source .venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "2. Open your browser and go to: http://127.0.0.1:8000"
echo ""
echo "3. Login with your superuser credentials"
echo ""
echo "4. Complete the organization setup:"
echo "   - Add your organization details"
echo "   - Upload organization logo"
echo "   - Create departments and job titles"
echo "   - Add employees"
echo ""
echo "📚 Documentation:"
echo "   - README.md - Complete system documentation"
echo "   - KENYAN_STATUTORY_COMPLIANCE.md - Compliance guide"
echo "   - SECURITY_IMPLEMENTATION.md - Security features"
echo "   - PAYSLIP_PRINTING_GUIDE.md - Printing setup"
echo ""
echo "🔧 Troubleshooting:"
echo "   If you encounter any issues, check the documentation files"
echo "   or ensure all dependencies are properly installed."
echo ""
echo "🇰🇪 Built for Kenya - Compliant with KRA, NSSF, SHIF & Housing Levy"
echo "=========================================================="
